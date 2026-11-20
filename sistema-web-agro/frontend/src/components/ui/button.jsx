// shadcn/ui Button pattern (MIT), adapted for AgroScope's Tailwind 3 theme.
import React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva } from 'class-variance-authority'
import { clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
const variants = cva('ui-button', { variants: { variant: { default: 'ui-button-primary', outline: 'ui-button-outline', ghost: 'ui-button-ghost' } }, defaultVariants: { variant: 'default' } })
export const Button = React.forwardRef(({ className, variant, asChild = false, type, ...props }, ref) => {
 const Comp = asChild ? Slot : 'button'
 return <Comp ref={ref} type={asChild ? undefined : type || 'button'} className={twMerge(clsx(variants({ variant }), className))} {...props} />
})
Button.displayName = 'Button'
