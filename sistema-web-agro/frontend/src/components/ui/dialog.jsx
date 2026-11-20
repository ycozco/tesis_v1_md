import { useEffect, useRef } from 'react'
import { X } from 'lucide-react'
// Native modal supplies focus containment, Escape handling and top-layer rendering.
export function Dialog({open,onClose,title,description,children}) {
 const ref=useRef(null)
 const close=useRef(onClose);close.current=onClose
 useEffect(()=>{if(!open)return;const previous=document.body.style.overflow;document.body.style.overflow='hidden';return()=>{document.body.style.overflow=previous}},[open])
 useEffect(()=>{const dialog=ref.current;if(open&&!dialog.open)dialog.showModal();if(!open&&dialog.open)dialog.close()},[open])
 return <dialog ref={ref} className="market-dialog" aria-labelledby="market-detail-title" aria-describedby="market-detail-description" onClose={()=>close.current()} onClick={e=>{if(e.target===ref.current){const r=ref.current.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)ref.current.close()}}}>
  <header className="market-dialog-header"><div><span>Mercado al día / Detalle</span><h2 id="market-detail-title">{title}</h2><p id="market-detail-description">{description}</p></div><button autoFocus aria-label="Cerrar detalle de mercado" onClick={()=>ref.current.close()}><X size={20}/></button></header>
  <div className="market-dialog-body">{children}</div>
 </dialog>
}
