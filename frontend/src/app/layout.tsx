import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'ScreenSage Architect - Cloud Edition',
  description: 'AI-powered screen analysis and automation assistant in the cloud',
  keywords: ['AI', 'automation', 'screen analysis', 'OCR', 'computer vision'],
  authors: [{ name: 'ScreenSage Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#87A96B',
  openGraph: {
    title: 'ScreenSage Architect - Cloud Edition',
    description: 'AI-powered screen analysis and automation assistant in the cloud',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ScreenSage Architect - Cloud Edition',
    description: 'AI-powered screen analysis and automation assistant in the cloud',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}