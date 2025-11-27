import React from 'react';
import { useNavigate } from 'react-router-dom';
import './PoliticaPrivacidad.css';

const PoliticaPrivacidad = () => {
  const navigate = useNavigate();

  return (
    <div className="politica-container">
      <div className="politica-header">
        <button onClick={() => navigate(-1)} className="btn-volver">
          ← Volver
        </button>
        <h1>Política de Privacidad</h1>
        <p className="fecha-actualizacion">Última actualización: 27 de noviembre de 2025</p>
      </div>

      <div className="politica-content">
        <section>
          <h2>1. INFORMACIÓN GENERAL</h2>
          <p>
            En <strong>Bot Visas Estudio</strong> (en adelante, "la Plataforma"), respetamos tu privacidad y 
            estamos comprometidos con la protección de tus datos personales. Esta Política de Privacidad describe 
            cómo recopilamos, usamos, almacenamos y protegemos tu información personal de acuerdo con el 
            Reglamento General de Protección de Datos (RGPD) de la Unión Europea.
          </p>
        </section>

        <section>
          <h2>2. RESPONSABLE DEL TRATAMIENTO</h2>
          <p><strong>Identidad:</strong> Bot Visas Estudio</p>
          <p><strong>Email de contacto:</strong> privacidad@botvisasestudio.com</p>
          <p><strong>Finalidad:</strong> Asesoramiento y gestión de solicitudes de visa de estudiante para España</p>
        </section>

        <section>
          <h2>3. DATOS QUE RECOPILAMOS</h2>
          <p>Recopilamos la siguiente información personal cuando te registras en nuestra plataforma:</p>
          
          <h3>3.1 Datos de Identificación Personal</h3>
          <ul>
            <li>Nombre completo</li>
            <li>Fecha de nacimiento</li>
            <li>Edad</li>
            <li>Nacionalidad</li>
            <li>País y ciudad de origen</li>
            <li>Número de pasaporte</li>
          </ul>

          <h3>3.2 Datos de Contacto</h3>
          <ul>
            <li>Dirección de email</li>
            <li>Número de teléfono</li>
          </ul>

          <h3>3.3 Datos Académicos</h3>
          <ul>
            <li>Carrera deseada</li>
            <li>Especialidad</li>
            <li>Nivel de español</li>
            <li>Tipo de visa solicitada</li>
          </ul>

          <h3>3.4 Datos Financieros</h3>
          <ul>
            <li>Fondos disponibles</li>
            <li>Fecha estimada de inicio de estudios</li>
          </ul>

          <h3>3.5 Documentos</h3>
          <ul>
            <li>Título académico (escaneado)</li>
            <li>Copia del pasaporte</li>
            <li>Extractos bancarios</li>
          </ul>
        </section>

        <section>
          <h2>4. FINALIDAD DEL TRATAMIENTO</h2>
          <p>Utilizamos tus datos personales para las siguientes finalidades:</p>
          <ul>
            <li><strong>Gestión de tu solicitud:</strong> Procesar y gestionar tu solicitud de visa de estudiante</li>
            <li><strong>Asesoramiento personalizado:</strong> Proporcionarte recomendaciones de cursos y universidades</li>
            <li><strong>Evaluación de elegibilidad:</strong> Calcular tu probabilidad de éxito en la solicitud de visa</li>
            <li><strong>Generación de documentos:</strong> Crear borradores de cartas y documentación necesaria</li>
            <li><strong>Comunicación:</strong> Enviarte actualizaciones sobre tu proceso y responder tus consultas</li>
            <li><strong>Cumplimiento legal:</strong> Cumplir con obligaciones legales y regulatorias</li>
          </ul>
        </section>

        <section>
          <h2>5. BASE LEGAL DEL TRATAMIENTO</h2>
          <p>El tratamiento de tus datos se basa en:</p>
          <ul>
            <li><strong>Consentimiento:</strong> Has dado tu consentimiento explícito al marcar la casilla de aceptación durante el registro</li>
            <li><strong>Ejecución de contrato:</strong> El tratamiento es necesario para la prestación de nuestros servicios</li>
            <li><strong>Interés legítimo:</strong> Para mejorar nuestros servicios y proporcionar asesoramiento personalizado</li>
          </ul>
        </section>

        <section>
          <h2>6. DESTINATARIOS DE LOS DATOS</h2>
          <p>Tus datos personales pueden ser compartidos con:</p>
          <ul>
            <li><strong>Instituciones educativas:</strong> Universidades y escuelas de idiomas con las que colaboramos</li>
            <li><strong>Autoridades:</strong> Consulados y embajadas de España cuando sea necesario para tu solicitud</li>
            <li><strong>Proveedores de servicios:</strong> Empresas que nos ayudan a operar la plataforma (hosting, email, etc.)</li>
            <li><strong>Asesores legales:</strong> Cuando sea necesario para cumplir con obligaciones legales</li>
          </ul>
          <p>
            <strong>Nota importante:</strong> Nunca vendemos ni alquilamos tus datos personales a terceros con fines comerciales.
          </p>
        </section>

        <section>
          <h2>7. TRANSFERENCIAS INTERNACIONALES</h2>
          <p>
            Tus datos pueden ser transferidos y procesados fuera del Espacio Económico Europeo (EEE). 
            En estos casos, garantizamos que se aplican medidas de seguridad adecuadas conforme al RGPD, 
            como cláusulas contractuales tipo aprobadas por la Comisión Europea.
          </p>
        </section>

        <section>
          <h2>8. PLAZO DE CONSERVACIÓN</h2>
          <p>Conservamos tus datos personales durante:</p>
          <ul>
            <li><strong>Datos activos:</strong> Mientras tu solicitud esté en proceso y hasta 2 años después de su finalización</li>
            <li><strong>Documentos:</strong> Según los plazos legales requeridos por las autoridades (mínimo 5 años)</li>
            <li><strong>Tras cancelación de cuenta:</strong> 30 días para permitir recuperación, luego se eliminan permanentemente</li>
          </ul>
        </section>

        <section>
          <h2>9. TUS DERECHOS</h2>
          <p>De acuerdo con el RGPD, tienes los siguientes derechos:</p>
          
          <div className="derechos-grid">
            <div className="derecho-item">
              <h4>🔍 Derecho de Acceso</h4>
              <p>Solicitar una copia de tus datos personales</p>
            </div>
            <div className="derecho-item">
              <h4>✏️ Derecho de Rectificación</h4>
              <p>Corregir datos inexactos o incompletos</p>
            </div>
            <div className="derecho-item">
              <h4>🗑️ Derecho de Supresión</h4>
              <p>Solicitar la eliminación de tus datos ("derecho al olvido")</p>
            </div>
            <div className="derecho-item">
              <h4>⏸️ Derecho de Limitación</h4>
              <p>Restringir el procesamiento de tus datos</p>
            </div>
            <div className="derecho-item">
              <h4>📤 Derecho de Portabilidad</h4>
              <p>Recibir tus datos en formato estructurado y transferirlos</p>
            </div>
            <div className="derecho-item">
              <h4>⛔ Derecho de Oposición</h4>
              <p>Oponerte al tratamiento de tus datos</p>
            </div>
          </div>

          <p>
            Para ejercer cualquiera de estos derechos, contacta con nosotros en: 
            <strong> privacidad@botvisasestudio.com</strong>
          </p>
          <p>
            Responderemos a tu solicitud en un plazo máximo de <strong>30 días</strong>.
          </p>
        </section>

        <section>
          <h2>10. MEDIDAS DE SEGURIDAD</h2>
          <p>Implementamos medidas técnicas y organizativas para proteger tus datos:</p>
          <ul>
            <li>🔒 Cifrado SSL/TLS en todas las comunicaciones</li>
            <li>🔐 Almacenamiento seguro en bases de datos protegidas con contraseña</li>
            <li>👥 Acceso restringido solo a personal autorizado</li>
            <li>📝 Registros de auditoría de acceso a datos</li>
            <li>🔄 Copias de seguridad regulares</li>
            <li>🛡️ Protección contra accesos no autorizados</li>
          </ul>
        </section>

        <section>
          <h2>11. COOKIES Y TECNOLOGÍAS SIMILARES</h2>
          <p>
            Nuestra plataforma utiliza cookies técnicas estrictamente necesarias para el funcionamiento del sitio:
          </p>
          <ul>
            <li><strong>Cookies de sesión:</strong> Para mantener tu sesión activa mientras navegas</li>
            <li><strong>Cookies de autenticación:</strong> Para recordar tu código de acceso (si autorizas)</li>
          </ul>
          <p>
            No utilizamos cookies de terceros para publicidad o seguimiento sin tu consentimiento explícito.
          </p>
        </section>

        <section>
          <h2>12. MENORES DE EDAD</h2>
          <p>
            Nuestra plataforma está destinada a personas mayores de 16 años. Si eres menor de 16 años, 
            necesitas el consentimiento de tus padres o tutores legales para utilizar nuestros servicios.
          </p>
        </section>

        <section>
          <h2>13. CAMBIOS EN LA POLÍTICA DE PRIVACIDAD</h2>
          <p>
            Nos reservamos el derecho de actualizar esta Política de Privacidad. Te notificaremos cualquier 
            cambio significativo por email o mediante aviso destacado en la plataforma. La fecha de la última 
            actualización aparece al inicio de este documento.
          </p>
        </section>

        <section>
          <h2>14. AUTORIDAD DE CONTROL</h2>
          <p>
            Si consideras que tus derechos de protección de datos han sido vulnerados, puedes presentar una 
            reclamación ante la autoridad de control competente:
          </p>
          <p>
            <strong>Agencia Española de Protección de Datos (AEPD)</strong><br />
            Web: <a href="https://www.aepd.es" target="_blank" rel="noopener noreferrer">www.aepd.es</a><br />
            Teléfono: 901 100 099 / 912 663 517
          </p>
        </section>

        <section>
          <h2>15. CONTACTO</h2>
          <p>Para cualquier consulta sobre esta Política de Privacidad o sobre el tratamiento de tus datos:</p>
          <div className="contacto-info">
            <p>📧 <strong>Email:</strong> privacidad@botvisasestudio.com</p>
            <p>📞 <strong>Teléfono:</strong> +34 XXX XXX XXX</p>
            <p>🌐 <strong>Web:</strong> www.botvisasestudio.com</p>
          </div>
        </section>

        <div className="consentimiento-recordatorio">
          <h3>📋 Recordatorio sobre tu Consentimiento</h3>
          <p>
            Al registrarte en nuestra plataforma y marcar la casilla de consentimiento, aceptas que tratemos 
            tus datos personales conforme a esta Política de Privacidad. Puedes retirar tu consentimiento en 
            cualquier momento contactándonos.
          </p>
        </div>
      </div>

      <div className="politica-footer">
        <button onClick={() => navigate(-1)} className="btn-volver-footer">
          Volver a la página anterior
        </button>
      </div>
    </div>
  );
};

export default PoliticaPrivacidad;
