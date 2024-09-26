import { UseChatHelpers } from 'ai/react'

import { Button } from '@/components/ui/button'
import { ExternalLink } from '@/components/external-link'
import { IconArrowRight } from '@/components/ui/icons'

export function EmptyScreen() {
  return (
    <div className="mx-auto max-w-2xl px-4">
      <div className="flex flex-col gap-2 rounded-lg border bg-background p-8">
        <h1 className="text-lg font-semibold gradient-text">
          Assistant Services Publics du Bénin
        </h1>
        <p className="leading-normal text-muted-foreground">
          Cet assistant est un chatbot intelligent créé pour vous aider à obtenir des informations sur les services publics offerts par le gouvernement du Bénin.
        </p>
        
        <p className="leading-normal text-muted-foreground">
          
        </p>
      </div>
    </div>
  )
}
