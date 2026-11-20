export function sessionReturnPath(value) {
  return typeof value === 'string' && /^\/(?!\/)/.test(value) && !/[\\\r\n]/.test(value) && value !== '/login' ? value : '/dashboard'
}
