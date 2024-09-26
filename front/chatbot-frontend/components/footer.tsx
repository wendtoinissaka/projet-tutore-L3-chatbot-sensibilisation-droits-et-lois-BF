import React from 'react'

import { cn } from '@/lib/utils'
import { ExternalLink } from '@/components/external-link'

export function FooterText({ className, ...props }: React.ComponentProps<'p'>) {
  return (
    <p
      className={cn(
        'px-2 text-center text-xs leading-normal text-muted-foreground',
        className
      )}
      {...props}
    >
      Créer dans le cadre du programme{' '}
      <ExternalLink href="https://www.linkedin.com/company/africatechuptour?originalSubdomain=ci">ATUT 2024</ExternalLink> par l'équipe Xandy.
    </p>
  )
}
