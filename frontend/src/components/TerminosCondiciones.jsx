import React from 'react';
import { useNavigate } from 'react-router-dom';
import './TerminosCondiciones.css';

const TerminosCondiciones = () => {
  const navigate = useNavigate();

  return (
    <div className="terminos-container">
      <div className="terminos-header">
        <button onClick={() => navigate(-1)} className="btn-volver">
          ← Volver
        </button>
        <h1>Términos y Condiciones de Uso</h1>
        <p className="fecha-actualizacion">Última actualización: 17 de agosto de 2026</p>
      </div>

      <div className="terminos-content">
        <section className="introduccion">
          <p>
            Bienvenido a <strong>Capital Iberia</strong>. Estos Términos y Condiciones de Uso (en adelante, "Términos")
            regulan el acceso y uso de nuestra plataforma de gestión de operaciones comerciales entre España y Cuba.
            Al registrarte y utilizar nuestros servicios, aceptas estos Términos en su totalidad.
          </p>
          <p className="destacado">
            SI NO ESTÁS DE ACUERDO CON ESTOS TÉRMINOS, POR FAVOR NO UTILICES NUESTRA PLATAFORMA.
          </p>
        </section>

        <section>
          <h2>1. DEFINICIONES</h2>
          <ul>
            <li><strong>Plataforma:</strong> Capital Iberia, sitio web y servicios asociados</li>
            <li><strong>Usuario / Inversor:</strong> Persona que se registra y utiliza la plataforma</li>
            <li><strong>Servicios:</strong> Presentación de operaciones comerciales, gestión de participaciones y seguimiento de capital</li>
            <li><strong>Operación:</strong> Cada proyecto comercial concreto (compraventa, exportación u otro) con condiciones, capital y plazo definidos</li>
            <li><strong>Contenido:</strong> Toda información, documentos, textos, imágenes y datos en la plataforma</li>
          </ul>
        </section>

        <section>
          <h2>2. ACEPTACIÓN DE LOS TÉRMINOS</h2>
          <p>Al hacer clic en "Acepto" durante el proceso de registro, confirmas que:</p>
          <ul>
            <li>Has leído, entendido y aceptas estos Términos y Condiciones</li>
            <li>Has leído y aceptas nuestra Política de Privacidad</li>
            <li>Eres persona física o jurídica con capacidad legal para contratar</li>
            <li>Proporcionarás información veraz y actualizada</li>
          </ul>
        </section>

        <section>
          <h2>3. DESCRIPCIÓN DE LOS SERVICIOS</h2>
          <p>Capital Iberia ofrece los siguientes servicios:</p>

          <div className="servicios-grid">
            <div className="servicio-item">
              <h4>📊 Operaciones Activas</h4>
              <p>Acceso al catálogo de operaciones comerciales con condiciones, capital y plazo</p>
            </div>
            <div className="servicio-item">
              <h4>💰 Participaciones</h4>
              <p>Solicitud y seguimiento de participaciones en operaciones concretas</p>
            </div>
            <div className="servicio-item">
              <h4>📈 Panel de Inversor</h4>
              <p>Seguimiento de capital, movimientos y estado de cada operación</p>
            </div>
            <div className="servicio-item">
              <h4>📄 Documentación</h4>
              <p>Acceso y gestión de documentación asociada a cada operación</p>
            </div>
            <div className="servicio-item">
              <h4>🔔 Notificaciones</h4>
              <p>Alertas sobre actualizaciones de operaciones y movimientos de capital</p>
            </div>
          </div>
        </section>

        <section>
          <h2>4. REGISTRO Y CUENTA DE USUARIO</h2>

          <h3>4.1 Proceso de Registro</h3>
          <p>Para utilizar nuestros servicios, debes:</p>
          <ul>
            <li>Completar el formulario de registro con información veraz y completa</li>
            <li>Aceptar estos Términos y nuestra Política de Privacidad</li>
            <li>Aceptar el consentimiento de tratamiento de datos</li>
          </ul>

          <h3>4.2 Credenciales de Acceso</h3>
          <p>
            Al completar el registro, recibirás acceso mediante email y contraseña personal.
            Tus credenciales son:
          </p>
          <ul>
            <li>Personales e intransferibles</li>
            <li>Tu responsabilidad mantenerlas seguras y confidenciales</li>
          </ul>

          <h3>4.3 Responsabilidades del Usuario</h3>
          <p>Te comprometes a:</p>
          <ul>
            <li>Mantener la confidencialidad de tus credenciales de acceso</li>
            <li>Notificarnos inmediatamente si detectas uso no autorizado de tu cuenta</li>
            <li>No compartir tu cuenta con terceros</li>
            <li>Actualizar tu información cuando sea necesario</li>
            <li>No utilizar la plataforma para fines ilegales o fraudulentos</li>
          </ul>
        </section>

        <section>
          <h2>5. VERACIDAD DE LA INFORMACIÓN</h2>
          <div className="alerta-importante">
            <h3>⚠️ DECLARACIÓN IMPORTANTE</h3>
            <p>
              Declaro que toda la información proporcionada (datos personales, financieros, documentación)
              es <strong>VERAZ, COMPLETA Y ACTUALIZADA</strong>.
            </p>
            <p>Entiendo que proporcionar información falsa o fraudulenta puede resultar en:</p>
            <ul>
              <li>❌ Cancelación inmediata de mi cuenta</li>
              <li>❌ Inhabilitación permanente de la plataforma</li>
              <li>❌ Posibles consecuencias legales</li>
            </ul>
          </div>
        </section>

        <section>
          <h2>6. NATURALEZA DEL SERVICIO Y LIMITACIONES</h2>

          <h3>6.1 Plataforma de Información</h3>
          <p className="destacado-importante">
            Capital Iberia es una plataforma de <strong>GESTIÓN E INFORMACIÓN</strong> sobre operaciones comerciales.
            NO somos una entidad financiera regulada ni ofrecemos asesoramiento de inversión homologado.
          </p>

          <h3>6.2 No Garantizamos Rentabilidad</h3>
          <p>
            <strong>NO GARANTIZAMOS</strong> rendimientos ni la recuperación del capital participado. Cada operación
            conlleva riesgo comercial y operativo. Los resultados dependen de cada operación concreta.
          </p>

          <h3>6.3 Información Orientativa</h3>
          <p>
            La información presentada en el catálogo de operaciones es orientativa. Las condiciones definitivas
            se negocian y documentan antes de formalizar cualquier participación.
          </p>
        </section>

        <section>
          <h2>7. OBLIGACIONES DEL USUARIO</h2>
          <p>Como usuario de la plataforma, te comprometes a:</p>
          <ul>
            <li>Proporcionar información veraz, completa y actualizada</li>
            <li>Responder a solicitudes de información adicional de manera oportuna</li>
            <li>Cumplir con los requisitos legales de tu país y España</li>
            <li>No utilizar la plataforma para actividades ilegales o fraudulentas</li>
            <li>Respetar los derechos de propiedad intelectual de la plataforma</li>
          </ul>
        </section>

        <section>
          <h2>8. PROPIEDAD INTELECTUAL</h2>
          <p>
            Todo el contenido de la plataforma (diseño, textos, gráficos, logos, código)
            es propiedad de Capital Iberia y está protegido por leyes de propiedad intelectual.
          </p>
          <p>Queda expresamente prohibido:</p>
          <ul>
            <li>Copiar, reproducir o distribuir el contenido sin autorización</li>
            <li>Realizar ingeniería inversa de la plataforma</li>
            <li>Crear obras derivadas del contenido</li>
            <li>Utilizar el contenido con fines comerciales sin permiso</li>
          </ul>
        </section>

        <section>
          <h2>9. PROTECCIÓN DE DATOS PERSONALES</h2>
          <p>
            El tratamiento de tus datos personales se rige por nuestra
            <strong> Política de Privacidad</strong>, que forma parte integral de estos Términos.
          </p>
          <p>Al utilizar la plataforma, aceptas que:</p>
          <ul>
            <li>Tus datos serán tratados conforme al RGPD</li>
            <li>Pueden ser compartidos con socios comerciales y autoridades cuando sea necesario</li>
            <li>Puedes ejercer tus derechos de acceso, rectificación, supresión, etc.</li>
          </ul>
        </section>

        <section>
          <h2>10. SUSPENSIÓN Y TERMINACIÓN DE CUENTA</h2>

          <h3>10.1 Suspensión por Incumplimiento</h3>
          <p>Podemos suspender o cancelar tu cuenta si:</p>
          <ul>
            <li>Proporcionas información falsa o fraudulenta</li>
            <li>Incumples estos Términos y Condiciones</li>
            <li>Utilizas la plataforma para actividades ilegales</li>
            <li>Intentas vulnerar la seguridad de la plataforma</li>
          </ul>

          <h3>10.2 Cancelación por el Usuario</h3>
          <p>
            Puedes solicitar la cancelación de tu cuenta en cualquier momento contactándonos.
            Tus datos serán eliminados conforme a nuestra Política de Privacidad.
          </p>
        </section>

        <section>
          <h2>11. LIMITACIÓN DE RESPONSABILIDAD</h2>
          <div className="limitacion-responsabilidad">
            <h3>⚖️ EXENCIÓN DE RESPONSABILIDAD</h3>
            <p>Capital Iberia NO se hace responsable de:</p>
            <ul>
              <li>❌ Pérdidas de capital derivadas del resultado de operaciones comerciales</li>
              <li>❌ Cambios en las condiciones del mercado o entorno comercial</li>
              <li>❌ Decisiones tomadas basadas exclusivamente en la información de la plataforma</li>
              <li>❌ Interrupciones temporales del servicio por mantenimiento</li>
              <li>❌ Problemas técnicos o fallos en la plataforma</li>
            </ul>
          </div>
        </section>

        <section>
          <h2>12. MODIFICACIONES DE LOS TÉRMINOS</h2>
          <p>
            Nos reservamos el derecho de modificar estos Términos en cualquier momento.
            Los cambios entrarán en vigor al ser publicados en la plataforma.
          </p>
          <p>Te notificaremos sobre cambios significativos mediante:</p>
          <ul>
            <li>Email a tu dirección registrada</li>
            <li>Aviso destacado en la plataforma</li>
            <li>Actualización de la fecha en este documento</li>
          </ul>
        </section>

        <section>
          <h2>13. LEY APLICABLE Y JURISDICCIÓN</h2>
          <p>
            Estos Términos se rigen por las leyes de <strong>España</strong>.
          </p>
          <p>
            Para la resolución de cualquier controversia, las partes se someten a los
            juzgados y tribunales de <strong>Madrid, España</strong>, renunciando a cualquier
            otro fuero que pudiera corresponderles.
          </p>
        </section>

        <section>
          <h2>14. RESOLUCIÓN DE CONFLICTOS</h2>
          <p>En caso de controversia o reclamación, las partes acuerdan intentar resolverla mediante:</p>
          <ol>
            <li><strong>Contacto directo:</strong> Comunicación con nuestro equipo</li>
            <li><strong>Mediación:</strong> Uso de servicios de mediación si el contacto directo no resuelve el problema</li>
            <li><strong>Vía judicial:</strong> Como último recurso, procedimientos legales ante tribunales competentes</li>
          </ol>
        </section>

        <section>
          <h2>15. CONTACTO Y SOPORTE</h2>
          <p>Para consultas, soporte o reclamaciones:</p>
          <div className="contacto-box">
            <p>📧 <strong>Email General:</strong> contacto@capitaliberia.com</p>
            <p>📧 <strong>Privacidad:</strong> privacidad@capitaliberia.com</p>
            <p>⏰ <strong>Horario:</strong> Lunes a Viernes, 9:00 - 18:00 (CET)</p>
          </div>
        </section>

        <section>
          <h2>16. DISPOSICIONES GENERALES</h2>

          <h3>16.1 Integridad del Acuerdo</h3>
          <p>
            Estos Términos, junto con la Política de Privacidad, constituyen el acuerdo completo
            entre tú y Capital Iberia.
          </p>

          <h3>16.2 Divisibilidad</h3>
          <p>Si alguna cláusula se declara inválida, las demás cláusulas seguirán en vigor.</p>

          <h3>16.3 Renuncia</h3>
          <p>La no exigencia de algún derecho no constituye renuncia al mismo.</p>

          <h3>16.4 Cesión</h3>
          <p>
            No puedes ceder tus derechos u obligaciones bajo estos Términos sin nuestro consentimiento previo.
          </p>
        </section>

        <div className="aceptacion-final">
          <h3>✅ ACEPTACIÓN</h3>
          <p>
            Al utilizar Capital Iberia, confirmas que has leído, entendido y aceptado estos
            Términos y Condiciones en su totalidad.
          </p>
          <p>
            Si tienes dudas sobre alguna cláusula, por favor contáctanos antes de usar la plataforma.
          </p>
        </div>
      </div>

      <div className="terminos-footer">
        <p className="version">Versión 2.0 - Agosto 2026</p>
        <button onClick={() => navigate(-1)} className="btn-volver-footer">
          Volver a la página anterior
        </button>
      </div>
    </div>
  );
};

export default TerminosCondiciones;
