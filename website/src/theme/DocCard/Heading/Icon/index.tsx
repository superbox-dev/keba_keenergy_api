import type {ReactNode} from 'react';
import clsx from 'clsx';
import isInternalUrl from '@docusaurus/isInternalUrl';
import {ThemeClassNames} from '@docusaurus/theme-common';
import type {PropSidebarItem} from '@docusaurus/plugin-content-docs';
import {ExternalLink, FileText, Folder, type LucideIcon} from 'lucide-react';

import styles from './styles.module.css';

type Props = {
  item: PropSidebarItem;
  icon: ReactNode;
};

// Line icons like on contributors.home-assistant.io instead of the emoji of Docusaurus
function iconOf(item: PropSidebarItem): LucideIcon {
  if (item.type === 'category') {
    return Folder;
  }

  return item.type === 'link' && !isInternalUrl(item.href) ? ExternalLink : FileText;
}

export default function DocCardHeadingIcon({item}: Props): ReactNode {
  const Icon: LucideIcon = iconOf(item);

  return (
    <span className={clsx(ThemeClassNames.docs.docCard.icon, styles.icon)}>
      <Icon size={20} strokeWidth={1.75} aria-hidden="true" />
    </span>
  );
}
