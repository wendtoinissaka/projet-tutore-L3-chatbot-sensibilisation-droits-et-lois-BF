import { ReactNode } from 'react';

// Fonction récursive pour récupérer le texte à partir d'un ReactNode
export function extractTextFromReactNode(node: ReactNode): string {
  if (typeof node === 'string' || typeof node === 'number') {
    return String(node);
  }

  if (Array.isArray(node)) {
    return node.map(extractTextFromReactNode).join('');
  }

  if (node && typeof node === 'object' && 'props' in node) {
    const children = (node as any).props.children;
    return extractTextFromReactNode(children);
  }

  return '';
}


//const text = extractTextFromReactNode(myNode);
//console.log(text); // "HelloWorld!"
