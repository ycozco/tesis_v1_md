import random
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models import SessionLocal, Usuario, SecurityLog, DecisionAuditoria
from services.common import USER_CONDITIONS

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = data.get('identifier')
    password = data.get('password')
    ip_addr = request.remote_addr or '127.0.0.1'

    if not identifier or not password:
        return jsonify({'message': 'Identificador y contraseña requeridos.'}), 400

    db = SessionLocal()
    try:
        user = db.query(Usuario).filter(
            (Usuario.username == identifier) | (Usuario.email == identifier)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            if user.rol == 'AUDITOR':
                if user.username not in USER_CONDITIONS:
                    USER_CONDITIONS[user.username] = random.choice(['INTEGRADO', 'AISLADO'])
                condicion = USER_CONDITIONS[user.username]
            else:
                condicion = 'ADMIN'

            sec_log = SecurityLog(usuario=user.username, evento='LOGIN_SUCCESS', ip_address=ip_addr)
            db.add(sec_log)
            db.commit()

            return jsonify({
                'token': f'mock-token-{user.id_usuario}',
                'user': user.to_dict(),
                'condicion': condicion
            }), 200
        else:
            sec_log = SecurityLog(usuario=identifier[:50], evento='LOGIN_FAILURE', ip_address=ip_addr)
            db.add(sec_log)
            db.commit()
            return jsonify({'message': 'Acceso denegado. Credenciales incorrectas.'}), 401
    except Exception as e:
        db.rollback()
        return jsonify({'message': f'Error en el servidor: {str(e)}'}), 500
    finally:
        db.close()

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    data = request.get_json() or {}
    username = data.get('username', 'anonymous')
    ip_addr = request.remote_addr or '127.0.0.1'

    db = SessionLocal()
    try:
        sec_log = SecurityLog(usuario=username, evento='LOGOUT', ip_address=ip_addr)
        db.add(sec_log)
        db.commit()
        return jsonify({'message': 'Sesión cerrada.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@auth_bp.route('/api/users/list', methods=['GET'])
def get_users_list():
    db = SessionLocal()
    try:
        users = db.query(Usuario).all()
        users_list = []
        for u in users:
            cond = USER_CONDITIONS.get(u.username, 'INTEGRADO') if u.rol == 'AUDITOR' else '-'
            last_log = db.query(SecurityLog).filter_by(usuario=u.username).order_by(SecurityLog.fecha.desc()).first()
            
            t_minus = "Desconectado"
            if last_log:
                diff = datetime.utcnow() - last_log.fecha
                if diff.days > 0:
                    t_minus = f"hace {diff.days}d"
                elif diff.seconds // 3600 > 0:
                    t_minus = f"hace {diff.seconds // 3600}h"
                elif diff.seconds // 60 > 0:
                    t_minus = f"hace {diff.seconds // 60}m"
                else:
                    t_minus = "hace segundos"

            users_list.append({
                'username': u.username,
                'nombre': u.nombre,
                'email': u.email,
                'rol': u.rol,
                'condicion': cond,
                'last_active': t_minus,
                'estado': 'ACTIVO' if last_log and diff.days < 7 else 'INACTIVO'
            })
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@auth_bp.route('/api/users/update-condition', methods=['POST'])
def update_user_condition():
    data = request.get_json() or {}
    username = data.get('username')
    condicion = data.get('condicion')

    if not username or condicion not in ['INTEGRADO', 'AISLADO']:
        return jsonify({'message': 'Usuario y condición válidos requeridos.'}), 400

    USER_CONDITIONS[username] = condicion
    
    db = SessionLocal()
    try:
        ip_addr = request.remote_addr or '127.0.0.1'
        sec_log = SecurityLog(
            usuario='SYSTEM',
            evento=f'CHANGE_CONDITION: {username} -> {condicion}',
            ip_address=ip_addr
        )
        db.add(sec_log)
        db.commit()
        return jsonify({'message': f'Condición de {username} actualizada a {condicion}.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@auth_bp.route('/api/users/logs', methods=['GET'])
def get_security_logs():
    db = SessionLocal()
    try:
        logs = db.query(SecurityLog).order_by(SecurityLog.fecha.desc()).limit(30).all()
        return jsonify([l.to_dict() for l in logs]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@auth_bp.route('/api/users/create', methods=['POST'])
def create_user():
    db = SessionLocal()
    try:
        data = request.get_json() or {}
        username = data.get('username')
        email = data.get('email')
        nombre = data.get('nombre')
        password = data.get('password')
        rol = data.get('rol', 'AUDITOR')
        
        if not username or not email or not password or not nombre:
            return jsonify({'message': 'Faltan campos obligatorios.'}), 400
            
        exist = db.query(Usuario).filter((Usuario.username == username) | (Usuario.email == email)).first()
        if exist:
            return jsonify({'message': 'Usuario o Email ya registrado.'}), 400
            
        hashed = generate_password_hash(password)
        new_user = Usuario(
            username=username,
            email=email,
            password_hash=hashed,
            rol=rol,
            nombre=nombre
        )
        db.add(new_user)
        db.commit()
        
        USER_CONDITIONS[username] = 'INTEGRADO'
        
        return jsonify({'message': 'Usuario operativo creado exitosamente.', 'user': new_user.to_dict()}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@auth_bp.route('/api/users/<username>/reset-telemetry', methods=['POST'])
def reset_user_telemetry(username):
    db = SessionLocal()
    try:
        user = db.query(Usuario).filter_by(username=username).first()
        if not user:
            return jsonify({'message': 'Usuario no encontrado.'}), 404
            
        db.query(DecisionAuditoria).filter_by(id_usuario=user.id_usuario).delete()
        db.commit()
        
        ip_addr = request.remote_addr or '127.0.0.1'
        sec_log = SecurityLog(
            usuario='SYSTEM',
            evento=f'RESET_TELEMETRY: {username}',
            ip_address=ip_addr
        )
        db.add(sec_log)
        db.commit()
        
        return jsonify({'message': f'Telemetría del usuario {username} reiniciada exitosamente.'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()
