import Image from 'next/image'
import Head from 'next/head';
import SignIn from '../components/SignIn.js';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Eyes to see!</title>
      </Head>

      <main>
        <SignIn />
      </main>
    </div>
  )
}
