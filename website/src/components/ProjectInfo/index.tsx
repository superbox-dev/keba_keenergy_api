import type {ReactNode} from 'react';
import Link from '@docusaurus/Link';
import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';
import {Bug, FileCode, Github, HeartHandshake, History, Lightbulb, Package} from 'lucide-react';

import styles from './styles.module.css';

const repository = 'https://github.com/superbox-dev/keba_keenergy_api';
const maintainer = 'mh-superbox';

// Project card above the table of contents, styled after the Home Assistant integration sidebar
export default function ProjectInfo(): ReactNode {
  return (
    <div className={styles.projectInfo}>
      <section className={styles.module}>
        <div className={styles.logo}>
          <ThemedImage
            className={styles.brand}
            alt="KEBA"
            sources={{light: useBaseUrl('/logo.png'), dark: useBaseUrl('/dark_logo.png')}}
            width={995}
            height={256}
          />
          <Link href="https://pypi.org/project/keba-keenergy-api/">
            <img
              src="https://img.shields.io/pypi/v/keba-keenergy-api?label=PyPI"
              alt="Latest version on PyPI"
              height={20}
            />
          </Link>
        </div>
        <p className={styles.section}>
          An asynchronous Python client for the KEBA KeEnergy Web HMI, used by the Home Assistant integration.
        </p>
        <p className={styles.section}>
          A community project, not affiliated with or endorsed by KEBA. KEBA is a registered trademark of its owner.
        </p>
        <p className={styles.section}>
          <FileCode className={styles.icon} aria-hidden="true" /> Requires Python 3.11 or newer.
        </p>
        <p className={styles.section}>
          <Link href={repository}>
            <Github className={styles.icon} aria-hidden="true" /> View source on GitHub
          </Link>
          <br />
          <Link href={`${repository}/issues?q=is%3Aissue+is%3Aopen+label%3Abug`}>
            <Bug className={styles.icon} aria-hidden="true" /> View known issues
          </Link>
          <br />
          <Link href={`${repository}/issues/new/choose`}>
            <Lightbulb className={styles.icon} aria-hidden="true" /> Request a feature
          </Link>
          <br />
          <Link href="https://pypi.org/project/keba-keenergy-api/">
            <Package className={styles.icon} aria-hidden="true" /> View on PyPI
          </Link>
          <br />
          <Link to="/changelog">
            <History className={styles.icon} aria-hidden="true" /> Changelog
          </Link>
        </p>
      </section>
      <section className={styles.module}>
        <h2 className={styles.title}>
          <HeartHandshake className={styles.icon} aria-hidden="true" /> Maintainer
        </h2>
        <Link className={styles.owner} href={`https://github.com/${maintainer}`}>
          <img src={`https://avatars.githubusercontent.com/${maintainer}?size=96`} alt="" width={32} height={32} />
          @{maintainer}
        </Link>
      </section>
    </div>
  );
}
