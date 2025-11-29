import { Menu, User } from "lucide-react"
import Link from "next/link"

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-teal-600 to-teal-800 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">EE</span>
              </div>
              <span className="font-bold text-gray-900 text-sm">ESTUDIA EN ESPAÑA</span>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center gap-8">
              <Link href="#" className="text-teal-500 font-medium text-sm">
                Inicio
              </Link>
              <Link href="#" className="text-gray-700 hover:text-gray-900 text-sm">
                Servicios
              </Link>
              <Link href="#" className="text-gray-700 hover:text-gray-900 text-sm">
                Universidades
              </Link>
              <Link href="#" className="text-gray-700 hover:text-gray-900 text-sm">
                Blog
              </Link>
              <Link href="#" className="text-gray-700 hover:text-gray-900 text-sm">
                Contacto
              </Link>
            </nav>

            {/* User Icon */}
            <div className="flex items-center gap-4">
              <button className="p-2 hover:bg-gray-100 rounded-lg">
                <User className="w-5 h-5 text-gray-700" />
              </button>
              <button className="md:hidden p-2 hover:bg-gray-100 rounded-lg">
                <Menu className="w-5 h-5 text-gray-700" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative h-96 md:h-[500px] bg-gray-900 overflow-hidden rounded-3xl mx-4 md:mx-8 mt-6">
        {/* Background Image */}
        <img
          src="https://images.unsplash.com/photo-1553531088-d35cf4f3b0c8?w=1200&h=600&fit=crop"
          alt="Campus"
          className="absolute inset-0 w-full h-full object-cover"
        />

        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-black/30"></div>

        {/* Content */}
        <div className="absolute inset-0 flex items-center">
          <div className="max-w-2xl px-8 md:px-12">
            {/* Semi-transparent container */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-4 leading-tight">
                Tu Puerta de
                <br />
                Entrada a Europa
              </h1>

              <p className="text-white/90 text-lg mb-8">
                Expertos en visas de estudio y admisión
                <br />
                universitaria en España
              </p>

              {/* Buttons */}
              <div className="flex flex-wrap gap-4">
                <button className="bg-teal-600 hover:bg-teal-700 text-white px-6 py-3 rounded-full font-medium transition">
                  Comenzar Trámite
                </button>
                <button className="border-2 border-white text-white hover:bg-white/10 px-6 py-3 rounded-full font-medium transition">
                  Más Información
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-16 px-4 md:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Service Card 1 */}
            <div className="bg-white rounded-2xl p-8 shadow-md hover:shadow-lg transition">
              <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-teal-100 to-teal-50 rounded-xl flex items-center justify-center">
                <div className="text-5xl">🎓</div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 text-center mb-3">Admisión Garantizada</h3>
              <p className="text-gray-600 text-center text-sm">Aseguramos tu plaza en universidades de prestigio.</p>
            </div>

            {/* Service Card 2 */}
            <div className="bg-white rounded-2xl p-8 shadow-md hover:shadow-lg transition">
              <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-teal-100 to-teal-50 rounded-xl flex items-center justify-center">
                <div className="text-5xl">📱</div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 text-center mb-3">Visa Express</h3>
              <p className="text-gray-600 text-center text-sm">Agılizamos tus trámites para un proceso sin estrés.</p>
            </div>

            {/* Service Card 3 */}
            <div className="bg-white rounded-2xl p-8 shadow-md hover:shadow-lg transition">
              <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-teal-100 to-teal-50 rounded-xl flex items-center justify-center">
                <div className="text-5xl">🏢</div>
              </div>
              <h3 className="text-xl font-bold text-gray-900 text-center mb-3">Alojamiento Premium</h3>
              <p className="text-gray-600 text-center text-sm">
                Opciones de vivienda seguras y confortables para estudiantes.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4 md:px-8">
        <div className="max-w-6xl mx-auto">
          {/* Footer Content */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 pb-8 border-b border-gray-700">
            {/* Links */}
            <nav className="flex flex-wrap gap-6 md:gap-8 mb-6 md:mb-0">
              <Link href="#" className="text-gray-300 hover:text-white text-sm">
                Inicio
              </Link>
              <Link href="#" className="text-gray-300 hover:text-white text-sm">
                Servicios
              </Link>
              <Link href="#" className="text-gray-300 hover:text-white text-sm">
                Universidades
              </Link>
              <Link href="#" className="text-gray-300 hover:text-white text-sm">
                Blog
              </Link>
              <Link href="#" className="text-gray-300 hover:text-white text-sm">
                Contacto
              </Link>
            </nav>

            {/* Social Icons */}
            <div className="flex gap-4">
              <a href="#" className="bg-gray-700 hover:bg-gray-600 p-2 rounded-full transition">
                <span className="text-white">f</span>
              </a>
              <a href="#" className="bg-gray-700 hover:bg-gray-600 p-2 rounded-full transition">
                <span className="text-white">𝕏</span>
              </a>
              <a href="#" className="bg-gray-700 hover:bg-gray-600 p-2 rounded-full transition">
                <span className="text-white">📷</span>
              </a>
              <a href="#" className="bg-gray-700 hover:bg-gray-600 p-2 rounded-full transition">
                <span className="text-white">▶</span>
              </a>
            </div>
          </div>

          {/* Contact Info */}
          <div className="flex flex-col md:flex-row gap-6 md:gap-12">
            <div className="flex items-center gap-3">
              <span className="text-gray-400">📞</span>
              <span className="text-gray-300 text-sm">+7 (3) 453 6780</span>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-gray-400">✉</span>
              <span className="text-gray-300 text-sm">estudia@españa.com</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
