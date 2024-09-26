import { Separator } from '@/components/ui/separator'
import { UIState } from '@/lib/chat/actions'
import { Session } from '@/lib/types'
import Link from 'next/link'
import { ExclamationTriangleIcon } from '@radix-ui/react-icons'
import AnimatedText from './animated-text'
import { extractTextFromReactNode } from '@/utils/extractTextFromReactNode'

export interface ChatList {
  messages: UIState
  session?: Session
  isShared: boolean
}

export function ChatList({ messages, session, isShared }: ChatList) {
  if (!messages.length) {
    return null
  }


  return (
    <div className="relative mx-auto max-w-2xl px-4">
      {!isShared && !session ? (
        <>
          <div className="group relative mb-4 flex items-start md:-ml-12">
            <div className="bg-background flex size-[25px] shrink-0 select-none items-center justify-center rounded-md border shadow-sm">
              <ExclamationTriangleIcon />
            </div>
            <div className="ml-4 flex-1 space-y-2 overflow-hidden px-1">
              <p className="text-muted-foreground leading-normal">
                Merci de{' '}
                <Link href="/login" className="underline">
                  créer un compte
                </Link>{' '}
                ou{' '}
                <Link href="/signup" className="underline">
                  de vous connecter
                </Link>{' '}
                pour sauvegarder votre historique.
              </p>
            </div>
          </div>
          <Separator className="my-4" />
        </>
      ) : null}

      {messages.map((message, index) => (
        <>
          <div key={message.id}>
            {message.display}
            {/* <AnimatedText text={extractTextFromReactNode(message.display)} /> */}
            {index < messages.length - 1 && <Separator className="my-4" />}
          </div>
        </>
        
      ))}
    </div>
  )
}
