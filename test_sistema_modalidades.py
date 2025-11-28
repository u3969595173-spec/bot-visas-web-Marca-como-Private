#!/usr/bin/env python3
"""
Script de prueba para el nuevo sistema de modalidades de pago
Valida el flujo completo desde solicitud hasta pago
"""

import requests
import json
import time
from datetime import datetime

# Configuración
BASE_URL = "http://127.0.0.1:8000"
HEADERS = {"Content-Type": "application/json"}

def test_flujo_completo():
    """Prueba el flujo completo del sistema de modalidades"""
    
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA DE MODALIDADES\n")
    
    # 1. Crear solicitud de presupuesto como estudiante
    print("1️⃣ CREANDO SOLICITUD DE PRESUPUESTO...")
    
    servicios_test = [
        "gestion_basica_documentos",
        "solicitud_universitaria", 
        "cita_preparacion_consular"
    ]
    
    solicitud = {
        "estudiante_id": 1,
        "servicios_solicitados": servicios_test,
        "descripcion": "Necesito ayuda con gestión básica, aplicación universitaria y preparación para la cita consular"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/presupuestos", 
                               headers=HEADERS, 
                               data=json.dumps(solicitud))
        
        if response.status_code == 200:
            presupuesto = response.json()
            presupuesto_id = presupuesto['id']
            print(f"   ✅ Presupuesto creado ID: {presupuesto_id}")
            print(f"   📋 Servicios solicitados: {', '.join(servicios_test)}")
        else:
            print(f"   ❌ Error creando presupuesto: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 2. Ofertar modalidades como admin
    print("\n2️⃣ ADMIN OFERTANDO MODALIDADES DE PAGO...")
    
    modalidades = {
        "precio_al_empezar": 1200.00,
        "precio_con_visa": 1350.00,
        "precio_financiado": 1500.00,
        "comentarios_admin": "Oferta especial por ser servicios múltiples. Incluye seguimiento personalizado."
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/admin/presupuestos/{presupuesto_id}/ofertar-modalidades",
                              headers=HEADERS,
                              data=json.dumps(modalidades))
        
        if response.status_code == 200:
            print("   ✅ Modalidades ofertadas exitosamente")
            print(f"   💰 Pago al empezar: €{modalidades['precio_al_empezar']}")
            print(f"   🎯 Pago con visa: €{modalidades['precio_con_visa']}")
            print(f"   📅 Pago financiado: €{modalidades['precio_financiado']}")
        else:
            print(f"   ❌ Error ofertando modalidades: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 3. Estudiante acepta una modalidad
    print("\n3️⃣ ESTUDIANTE ACEPTANDO MODALIDAD...")
    
    respuesta = {
        "accion": "aceptar",
        "modalidad_seleccionada": "precio_con_visa",
        "comentarios": "Acepto la modalidad de pago al obtener la visa"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/presupuestos/{presupuesto_id}/respuesta",
                              headers=HEADERS,
                              data=json.dumps(respuesta))
        
        if response.status_code == 200:
            print("   ✅ Modalidad aceptada exitosamente")
            print(f"   🎯 Modalidad seleccionada: {respuesta['modalidad_seleccionada']}")
        else:
            print(f"   ❌ Error aceptando modalidad: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 4. Verificar tesoro de pagos como admin
    print("\n4️⃣ VERIFICANDO TESORO DE PAGOS...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/admin/tesoro")
        
        if response.status_code == 200:
            tesoro = response.json()
            print("   ✅ Tesoro de pagos accesible")
            
            # Buscar nuestro presupuesto
            for pago in tesoro:
                if pago['presupuesto_id'] == presupuesto_id:
                    print(f"   💰 Pago encontrado - ID: {pago['presupuesto_id']}")
                    print(f"   👤 Cliente: {pago['estudiante_nombre']}")
                    print(f"   💵 Monto: €{pago['monto_total']}")
                    print(f"   🏦 Estado pago: {'✅ Pagado' if pago['pagado'] else '⏳ Pendiente'}")
                    break
        else:
            print(f"   ❌ Error accediendo tesoro: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 5. Marcar como pagado
    print("\n5️⃣ ADMIN MARCANDO COMO PAGADO...")
    
    try:
        response = requests.put(f"{BASE_URL}/api/admin/tesoro/{presupuesto_id}/marcar-pagado")
        
        if response.status_code == 200:
            print("   ✅ Marcado como pagado exitosamente")
        else:
            print(f"   ❌ Error marcando como pagado: {response.text}")
            return
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return
    
    # 6. Verificación final
    print("\n6️⃣ VERIFICACIÓN FINAL DEL TESORO...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/admin/tesoro")
        
        if response.status_code == 200:
            tesoro = response.json()
            
            for pago in tesoro:
                if pago['presupuesto_id'] == presupuesto_id:
                    print(f"   🏦 Estado final: {'✅ PAGADO' if pago['pagado'] else '⏳ Pendiente'}")
                    print(f"   📅 Fecha pago: {pago.get('fecha_pago', 'No registrada')}")
                    break
        else:
            print(f"   ❌ Error en verificación final: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
    
    print(f"\n🎉 PRUEBA COMPLETADA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def mostrar_servicios_disponibles():
    """Muestra los 9 servicios disponibles en el sistema"""
    
    servicios = {
        "gestion_basica_documentos": "Gestión Básica de Documentos - Organización y revisión de documentación inicial",
        "solicitud_universitaria": "Solicitud Universitaria - Aplicación completa a universidades",
        "legalizacion_apostillamiento": "Legalización y Apostillamiento - Certificación internacional de documentos",
        "antecedentes_penales": "Antecedentes Penales - Gestión de certificados penales",
        "cita_preparacion_consular": "Cita y Preparación Consular - Programación y preparación para entrevista",
        "seguimiento_visa": "Seguimiento Hasta Visa Otorgada - Acompañamiento completo del proceso",
        "alojamiento": "Gestión de Alojamiento - Solo para cita consular",
        "seguro_medico": "Seguro Médico - Cobertura internacional para estudiantes",
        "financiacion": "Financiación - Solo para cita consular"
    }
    
    print("\n📋 SERVICIOS DISPONIBLES EN EL SISTEMA:")
    print("=" * 60)
    
    for codigo, descripcion in servicios.items():
        print(f"• {codigo}: {descripcion}")
    
    print("=" * 60)

if __name__ == "__main__":
    mostrar_servicios_disponibles()
    test_flujo_completo()