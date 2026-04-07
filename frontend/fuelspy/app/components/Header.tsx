import Link from 'next/link';
import Image from 'next/image';

export function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-2xl mx-auto px-6 py-4 flex justify-center">
        <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition">
          <Image src="/icon.svg" alt="FuelSpy" width={40} height={40} />
          <span className="text-2xl font-bold bg-gradient-to-r from-orange-400 to-orange-600 bg-clip-text text-transparent">
            FuelSpy
          </span>
        </Link>
      </div>
    </header>
  );
}