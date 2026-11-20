// Radix Tabs with the shadcn/ui composition pattern (MIT).
import React from 'react'
import * as Primitive from '@radix-ui/react-tabs'
export const Tabs = Primitive.Root
export const TabsList = React.forwardRef(({className = '', ...props}, ref) => <Primitive.List ref={ref} className={`research-segmented ${className}`} {...props} />)
export const TabsTrigger = Primitive.Trigger
export const TabsContent = Primitive.Content
TabsList.displayName = 'TabsList'
