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
        <p className="fecha-actualizacion">Última actualización: 27 de noviembre de 2025</p>
      </div>

      <div className="terminos-content">
        <section className="introduccion">
          <p>
            Bienvenido a <strong>Estudia en España</strong>. Estos Términos y Condiciones de Uso (en adelante, "Términos") 
            regulan el acceso y uso de nuestra plataforma de asesoramiento para solicitudes de visa de estudiante para España. 
            Al registrarte y utilizar nuestros servicios, aceptas estos Términos en su totalidad.
          </p>
          <p className="destacado">
            SI NO ESTÁS DE ACUERDO CON ESTOS TÉRMINOS, POR FAVOR NO UTILICES NUESTRA PLATAFORMA.
          </p>
        </section>

        <section>
          <h2>1. DEFINICIONES</h2>
          <ul>
            <li><strong>Plataforma:</strong> Estudia en España, sitio web y servicios asociados</li>
            <li><strong>Usuario:</strong> Persona que se registra y utiliza la plataforma</li>
            <li><strong>Servicios:</strong> Asesoramiento, gestión de documentos, recomendaciones y seguimiento de solicitud de visa</li>
            <li><strong>Contenido:</strong> Toda información, documentos, textos, imágenes y datos en la plataforma</li>
          </ul>
        </section>

        <section>
          <h2>2. ACEPTACIÓN DE LOS TÉRMINOS</h2>
          <p>
            Al hacer clic en "Acepto" durante el proceso de registro, o al utilizar cualquier servicio de la plataforma, 
            confirmas que:
          </p>
          <ul>
            <li>Has leído, entendido y aceptas estos Términos y Condiciones</li>
            <li>Has leído y aceptas nuestra Política de Privacidad</li>
            <li>Tienes al menos 16 años de edad (o cuentas con el consentimiento de tus padres/tutores)</li>
            <li>Proporcionarás información veraz y actualizada</li>
            <li>Eres legalmente capaz de celebrar contratos vinculantes</li>
          </ul>
        </section>

        <section>
          <h2>3. DESCRIPCIÓN DE LOS SERVICIOS</h2>
          <p>Estudia en España ofrece los siguientes servicios:</p>
          
          <div className="servicios-grid">
            <div className="servicio-item">
              <h4>📋 Gestión de Solicitudes</h4>
              <p>Procesamiento y seguimiento de tu solicitud de visa de estudiante</p>
            </div>
            <div className="servicio-item">
              <h4>🎓 Recomendaciones</h4>
              <p>Sugerencias personalizadas de cursos y universidades</p>
            </div>
            <div className="servicio-item">
              <h4>📊 Evaluación</h4>
              <p>Cálculo de probabilidad de éxito de tu solicitud</p>
            </div>
            <div className="servicio-item">
              <h4>📄 Documentos</h4>
              <p>Generación de borradores de documentación necesaria</p>
            </div>
            <div className="servicio-item">
              <h4>💬 Asesoramiento</h4>
              <p>Orientación sobre requisitos y proceso de solicitud</p>
            </div>
            <div className="servicio-item">
              <h4>🔔 Notificaciones</h4>
              <p>Alertas sobre actualizaciones y pasos pendientes</p>
            </div>
          </div>
        </section>

        <section>
          <h2>4. REGISTRO Y CUENTA DE USUARIO</h2>
          
          <h3>4.1 Proceso de Registro</h3>
          <p>Para utilizar nuestros servicios, debes:</p>
          <ul>
            <li>Completar el formulario de registro con información veraz y completa</li>
            <li>Proporcionar documentos válidos (pasaporte, títulos académicos, extractos bancarios)</li>
            <li>Aceptar estos Términos y nuestra Política de Privacidad</li>
            <li>Aceptar el consentimiento GDPR</li>
          </ul>

          <h3>4.2 Código de Acceso</h3>
          <p>
            Al completar el registro, recibirás un <strong>código de acceso único</strong> de 8 caracteres. 
            Este código es:
          </p>
          <ul>
            <li>Personal e intransferible</li>
            <li>Necesario para acceder a tu perfil</li>
            <li>Tu responsabilidad mantenerlo seguro y confidencial</li>
          </ul>

          <h3>4.3 Responsabilidades del Usuario</h3>
          <p>Te comprometes a:</p>
          <ul>
            <li>Mantener la confidencialidad de tu código de acceso</li>
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
              Declaro que toda la información proporcionada (datos personales, documentos, información financiera, 
              académica) es <strong>VERAZ, COMPLETA Y ACTUALIZADA</strong>.
            </p>
            <p>
              Entiendo que proporcionar información falsa o fraudulenta puede resultar en:
            </p>
            <ul>
              <li>❌ Rechazo de mi solicitud de visa</li>
              <li>❌ Cancelación inmediata de mi cuenta</li>
              <li>❌ Inhabilitación permanente de la plataforma</li>
              <li>❌ Posibles consecuencias legales</li>
              <li>❌ Prohibición de entrada a España</li>
            </ul>
          </div>
        </section>

        <section>
          <h2>6. NATURALEZA DEL SERVICIO Y LIMITACIONES</h2>
          
          <h3>6.1 Servicio de Asesoramiento</h3>
          <p className="destacado-importante">
            Estudia en España es una plataforma de <strong>ASESORAMIENTO Y GESTIÓN</strong>. 
            NO somos una agencia gubernamental ni tomamos decisiones sobre visas.
          </p>

          <h3>6.2 No Garantizamos Aprobación</h3>
          <p>
            <strong>NO GARANTIZAMOS</strong> la aprobación de tu visa de estudiante. La decisión final 
            corresponde exclusivamente al Consulado o Embajada de España en tu país.
          </p>

          <h3>6.3 Documentos Borrador</h3>
          <p>
            Los documentos generados por la plataforma son <strong>BORRADORES</strong> y deben ser:
          </p>
          <ul>
            <li>Revisados y completados con información oficial</li>
            <li>Firmados por las autoridades o instituciones correspondientes</li>
            <li>Apostillados cuando sea requerido</li>
            <li>Validados por un profesional legal si es necesario</li>
          </ul>

          <h3>6.4 Recomendaciones de Cursos</h3>
          <p>
            Las sugerencias de cursos y universidades son orientativas. Debes verificar directamente con 
            las instituciones educativas sobre requisitos, costos, disponibilidad y procesos de admisión.
          </p>
        </section>

        <section>
          <h2>7. OBLIGACIONES DEL USUARIO</h2>
          <p>Como usuario de la plataforma, te comprometes a:</p>
          <ul>
            <li>Proporcionar información veraz, completa y actualizada</li>
            <li>Subir documentos auténticos y válidos</li>
            <li>Responder a solicitudes de información adicional de manera oportuna</li>
            <li>Seguir las instrucciones y recomendaciones proporcionadas</li>
            <li>Cumplir con los requisitos legales de tu país y España</li>
            <li>Informar sobre cambios en tu situación que puedan afectar tu solicitud</li>
            <li>No utilizar la plataforma para actividades ilegales o fraudulentas</li>
            <li>Respetar los derechos de propiedad intelectual de la plataforma</li>
          </ul>
        </section>

        <section>
          <h2>8. PROPIEDAD INTELECTUAL</h2>
          <p>
            Todo el contenido de la plataforma (diseño, textos, gráficos, logos, código, algoritmos) 
            es propiedad de Estudia en España y está protegido por leyes de propiedad intelectual.
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
            <li>Pueden ser compartidos con instituciones educativas y autoridades cuando sea necesario</li>
            <li>Puedes ejercer tus derechos de acceso, rectificación, supresión, etc.</li>
          </ul>
        </section>

        <section>
          <h2>10. TARIFAS Y PAGOS</h2>
          
          <h3>10.1 Servicios Gratuitos</h3>
          <p>Actualmente, los servicios básicos de la plataforma son gratuitos, incluyendo:</p>
          <ul>
            <li>Registro y gestión de perfil</li>
            <li>Evaluación de probabilidad de éxito</li>
            <li>Recomendaciones de cursos</li>
            <li>Generación de documentos borrador</li>
          </ul>

          <h3>10.2 Servicios Premium (Futuro)</h3>
          <p>
            Nos reservamos el derecho de introducir servicios premium de pago en el futuro. 
            Se te notificará con antelación y podrás decidir si deseas contratarlos.
          </p>
        </section>

        <section>
          <h2>11. SUSPENSIÓN Y TERMINACIÓN DE CUENTA</h2>
          
          <h3>11.1 Suspensión por Incumplimiento</h3>
          <p>Podemos suspender o cancelar tu cuenta si:</p>
          <ul>
            <li>Proporcionas información falsa o fraudulenta</li>
            <li>Incumples estos Términos y Condiciones</li>
            <li>Utilizas la plataforma para actividades ilegales</li>
            <li>Intentas vulnerar la seguridad de la plataforma</li>
            <li>No respondes a solicitudes de verificación</li>
          </ul>

          <h3>11.2 Cancelación por el Usuario</h3>
          <p>
            Puedes solicitar la cancelación de tu cuenta en cualquier momento contactándonos. 
            Tus datos serán eliminados conforme a nuestra Política de Privacidad.
          </p>
        </section>

        <section>
          <h2>12. LIMITACIÓN DE RESPONSABILIDAD</h2>
          <div className="limitacion-responsabilidad">
            <h3>⚖️ EXENCIÓN DE RESPONSABILIDAD</h3>
            <p>Estudia en España NO se hace responsable de:</p>
            <ul>
              <li>❌ Rechazos de solicitud de visa por parte de las autoridades</li>
              <li>❌ Errores u omisiones en los documentos si no verificas el contenido</li>
              <li>❌ Cambios en requisitos legales o políticas de inmigración</li>
              <li>❌ Información desactualizada de instituciones educativas</li>
              <li>❌ Decisiones tomadas basándote únicamente en nuestras recomendaciones</li>
              <li>❌ Pérdidas económicas derivadas de rechazos de visa</li>
              <li>❌ Interrupciones temporales del servicio por mantenimiento</li>
              <li>❌ Problemas técnicos o fallos en la plataforma</li>
            </ul>
          </div>
        </section>

        <section>
          <h2>13. MODIFICACIONES DE LOS TÉRMINOS</h2>
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
          <p>
            El uso continuado de la plataforma después de las modificaciones constituye tu 
            aceptación de los nuevos términos.
          </p>
        </section>

        <section>
          <h2>14. LEY APLICABLE Y JURISDICCIÓN</h2>
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
          <h2>15. RESOLUCIÓN DE CONFLICTOS</h2>
          <p>
            En caso de controversia o reclamación, las partes acuerdan intentar resolverla mediante:
          </p>
          <ol>
            <li><strong>Contacto directo:</strong> Comunicación con nuestro equipo de soporte</li>
            <li><strong>Mediación:</strong> Uso de servicios de mediación si el contacto directo no resuelve el problema</li>
            <li><strong>Vía judicial:</strong> Como último recurso, procedimientos legales ante tribunales competentes</li>
          </ol>
        </section>

        <section>
          <h2>16. CONTACTO Y SOPORTE</h2>
          <p>Para consultas, soporte o reclamaciones:</p>
          <div className="contacto-box">
            <p>📧 <strong>Email General:</strong> info@botvisasestudio.com</p>
            <p>📧 <strong>Soporte Técnico:</strong> soporte@botvisasestudio.com</p>
            <p>📧 <strong>Datos Personales:</strong> privacidad@botvisasestudio.com</p>
            <p>📞 <strong>Teléfono:</strong> +34 XXX XXX XXX</p>
            <p>⏰ <strong>Horario:</strong> Lunes a Viernes, 9:00 - 18:00 (CET)</p>
          </div>
        </section>

        <section>
          <h2>17. DISPOSICIONES GENERALES</h2>
          
          <h3>17.1 Integridad del Acuerdo</h3>
          <p>
            Estos Términos, junto con la Política de Privacidad, constituyen el acuerdo completo 
            entre tú y Estudia en España.
          </p>

          <h3>17.2 Divisibilidad</h3>
          <p>
            Si alguna cláusula se declara inválida, las demás cláusulas seguirán en vigor.
          </p>

          <h3>17.3 Renuncia</h3>
          <p>
            La no exigencia de algún derecho no constituye renuncia al mismo.
          </p>

          <h3>17.4 Cesión</h3>
          <p>
            No puedes ceder tus derechos u obligaciones bajo estos Términos sin nuestro consentimiento previo.
          </p>
        </section>

        <div className="aceptacion-final">
          <h3>✅ ACEPTACIÓN</h3>
          <p>
            Al utilizar Estudia en España, confirmas que has leído, entendido y aceptado estos 
            Términos y Condiciones en su totalidad.
          </p>
          <p>
            Si tienes dudas sobre alguna cláusula, por favor contáctanos antes de usar la plataforma.
          </p>
        </div>
      </div>

      <div className="terminos-footer">
        <p className="version">Versión 1.0 - Noviembre 2025</p>
        <button onClick={() => navigate(-1)} className="btn-volver-footer">
          Volver a la página anterior
        </button>
      </div>
    </div>
  );
};

export default TerminosCondiciones;
