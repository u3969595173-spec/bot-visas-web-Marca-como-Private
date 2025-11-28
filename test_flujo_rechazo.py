#!/usr/bin/env python3
"""
Script de prueba para el flujo de rechazo y nueva solicitud
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
HEADERS = {"Content-Type": "application/json"}

def test_flujo_rechazo_nueva_solicitud():
    """Prueba el flujo completo: solicitud -> oferta -> rechazo -> nueva solicitud"""
    
    print("🧪 PROBANDO FLUJO DE RECHAZO Y NUEVA SOLICITUD")
    print("=" * 60)
    
    # 1. Primera solicitud
    print("\n1️⃣ CREANDO PRIMERA SOLICITUD DE PRESUPUESTO...")
    
    solicitud1 = {
        "estudiante_id": 2,
        "servicios_solicitados": ["gestion_basica_documentos", "solicitud_universitaria"],
        "descripcion": "Primera solicitud - Necesito gestión básica y aplicación universitaria"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/presupuestos", 
                               headers=HEADERS, 
                               data=json.dumps(solicitud1))
        
        if response.status_code == 200:
            presupuesto1 = response.json()
            presupuesto1_id = presupuesto1['id']
            print(f"   ✅ Primera solicitud creada - ID: {presupuesto1_id}")
        else:
            print(f"   ❌ Error creando primera solicitud: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 2. Admin oferta modalidades para primera solicitud
    print("\n2️⃣ ADMIN OFERTANDO MODALIDADES PARA PRIMERA SOLICITUD...")
    
    modalidades1 = {
        "precio_al_empezar": 800.00,
        "precio_con_visa": 900.00,
        "precio_financiado": 1000.00,
        "comentarios_admin": "Oferta inicial para gestión básica + aplicación universitaria"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/admin/presupuestos/{presupuesto1_id}/ofertar-modalidades",
                              headers=HEADERS,
                              data=json.dumps(modalidades1))
        
        if response.status_code == 200:
            print("   ✅ Primera oferta enviada con nota de rechazo incluida")
            print(f"   💰 Precios: €{modalidades1['precio_al_empezar']} / €{modalidades1['precio_con_visa']} / €{modalidades1['precio_financiado']}")
        else:
            print(f"   ❌ Error enviando primera oferta: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 3. Estudiante RECHAZA primera oferta
    print("\n3️⃣ ESTUDIANTE RECHAZANDO PRIMERA OFERTA...")
    
    rechazo = {
        "accion": "rechazar",
        "comentarios": "Los precios son muy altos para mi presupuesto"
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/presupuestos/{presupuesto1_id}/respuesta",
                              headers=HEADERS,
                              data=json.dumps(rechazo))
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Primera oferta rechazada exitosamente")
            print(f"   📝 Mensaje: {result.get('mensaje', '')}")
        else:
            print(f"   ❌ Error rechazando oferta: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 4. Estudiante hace NUEVA solicitud después del rechazo
    print("\n4️⃣ ESTUDIANTE HACIENDO NUEVA SOLICITUD DESPUÉS DEL RECHAZO...")
    
    solicitud2 = {
        "estudiante_id": 2,  # Mismo estudiante
        "servicios_solicitados": ["gestion_basica_documentos", "cita_preparacion_consular"],
        "descripcion": "Nueva solicitud después de rechazo - Cambié las opciones para ajustar mi presupuesto"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/presupuestos", 
                               headers=HEADERS, 
                               data=json.dumps(solicitud2))
        
        if response.status_code == 200:
            presupuesto2 = response.json()
            presupuesto2_id = presupuesto2['id']
            print(f"   ✅ Nueva solicitud creada exitosamente - ID: {presupuesto2_id}")
            print(f"   📋 Nuevos servicios: {', '.join(solicitud2['servicios_solicitados'])}")
        else:
            print(f"   ❌ Error creando nueva solicitud: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 5. Admin oferta modalidades para nueva solicitud
    print("\n5️⃣ ADMIN OFERTANDO MODALIDADES PARA NUEVA SOLICITUD...")
    
    modalidades2 = {
        "precio_al_empezar": 500.00,
        "precio_con_visa": 600.00, 
        "precio_financiado": 700.00,
        "comentarios_admin": "Nueva oferta ajustada a tu presupuesto. Servicios optimizados."
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/admin/presupuestos/{presupuesto2_id}/ofertar-modalidades",
                              headers=HEADERS,
                              data=json.dumps(modalidades2))
        
        if response.status_code == 200:
            print("   ✅ Nueva oferta enviada con nota de rechazo incluida")
            print(f"   💰 Nuevos precios: €{modalidades2['precio_al_empezar']} / €{modalidades2['precio_con_visa']} / €{modalidades2['precio_financiado']}")
        else:
            print(f"   ❌ Error enviando nueva oferta: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # 6. Estudiante ACEPTA la nueva oferta
    print("\n6️⃣ ESTUDIANTE ACEPTANDO NUEVA OFERTA...")
    
    aceptacion = {
        "accion": "aceptar",
        "modalidad_seleccionada": "precio_con_visa",
        "comentarios": "Perfecto! Esta oferta se ajusta a mi presupuesto. Acepto pago con visa."
    }
    
    try:
        response = requests.put(f"{BASE_URL}/api/presupuestos/{presupuesto2_id}/respuesta",
                              headers=HEADERS,
                              data=json.dumps(aceptacion))
        
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Nueva oferta aceptada exitosamente")
            print(f"   🎯 Modalidad: {aceptacion['modalidad_seleccionada']}")
            print(f"   📝 Mensaje: {result.get('mensaje', '')}")
        else:
            print(f"   ❌ Error aceptando nueva oferta: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    print(f"\n🎉 FLUJO COMPLETO EXITOSO - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("✅ El estudiante pudo:")
    print("   1. Hacer solicitud inicial")
    print("   2. Recibir oferta con nota de rechazo")
    print("   3. Rechazar la primera oferta")
    print("   4. Hacer nueva solicitud sin problemas")
    print("   5. Recibir nueva oferta ajustada")
    print("   6. Aceptar la nueva propuesta")
    print("=" * 60)

if __name__ == "__main__":
    test_flujo_rechazo_nueva_solicitud()