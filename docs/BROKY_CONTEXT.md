# Broky: El Agente Inmobiliario Digital

## 🎯 ¿Qué es Broky?

Broky es un agente inmobiliario digital que transforma la experiencia de vender o arrendar propiedades, combinando lo mejor de la intermediación profesional sin intermediarios físicos.

**El concepto central**: Desde WhatsApp, el propietario obtiene todo lo que necesita para publicar su propiedad + un afiche físico para su ventana + gestión automática de todos los interesados 24/7.

## 🏠 Cómo Funciona

### Para el Vendedor/Arrendador:
1. **Conversación Inicial**: Broky extrae información del inmueble mediante preguntas naturales + solicita fotos
2. **Avalúo Inmediato**: Genera automáticamente:
   - Valor comercial estimado del inmueble
   - Valor sugerido de arriendo
   - Sugerencias financieras según inmueble y sector
3. **Entregables Instantáneos**:
   - Afiche físico para imprimir y pegar en ventana (con QR y branding Broky)
   - Ficha técnica del inmueble
   - Creativos para redes sociales (WhatsApp Status, Facebook, Instagram)
   - Publicación en portales inmobiliarios
4. **Gestión de Interesados**: Broky atiende a TODOS los contactos del QR, califica perfiles y notifica al propietario

### Para el Comprador/Arrendatario:
1. **Contacto Directo**: Escanea QR del afiche → llega directo a Broky en WhatsApp
2. **Atención 24/7**: Broky responde dudas, envía información adicional, fotos, videos
3. **Calificación**: Broky evalúa el perfil del interesado según criterios del propietario
4. **Agenda Automática**: Si hay match, agenda visitas en horarios disponibles del propietario

## 🔄 Flujo Específico del MVP

### Fase 1: Captura de Información
```
Propietario → "Quiero arrendar/vender mi apartamento"
Broky → Extrae información básica conversacionalmente:
• Ubicación exacta
• Tipo de propiedad (casa/apto/local)
• Metros cuadrados
• Habitaciones/baños
• Precio deseado (inicial)
• Fotos principales
• Características especiales
• Preferencias de inquilino/comprador
```

### Fase 2: Avalúo y Sugerencias
```
Broky analiza con metodología de comparables usando portales:
• Valor comercial estimado
• Rango de precios del sector  
• Sugerencia de precio de arriendo
• Recomendaciones financieras
• Proyección de tiempo en mercado
```

### Fase 3: Generación de Materiales
```
Broky entrega:
• Afiche PDF listo para imprimir (con QR único)
• Ficha del inmueble profesional
• Posts para redes sociales
• Descripción para portales inmobiliarios
```

### Fase 4: Gestión de Interesados
```
Cada persona que escanea el QR:
• Llega a conversación con Broky
• Broky califica automáticamente
• Recolecta información del perfil
• Notifica al propietario con resumen
• Propietario elige a quién agendar
• Broky coordina visitas automáticamente
```

## 💰 Modelo de Negocio

### Estrategia Inicial: Freemium
- **Servicio Core Gratuito**: Avalúo + afiche + gestión básica de interesados
- **Revenue Streams**:
  - Servicios premium por fracción del costo tradicional
  - Gestión completa de visitas
  - Redacción de contratos
  - Trámites legales y cambios de servicios
  - Seguros y pólizas
  - Administración de arriendos
  - Data insights del mercado

### Comparación con Mercado Tradicional (Bogotá):
- **Broker tradicional**: 3-4% venta, 8-12% administración arriendo
- **Broky**: Fracción de estos costos con mayor eficiencia

## 🎯 Propuesta de Valor

### Lo que resuelve Broky:
1. **Elimina fricción**: No salir de WhatsApp para todo el proceso
2. **Mantiene tradición**: El afiche en ventana sigue siendo protagonista
3. **Escala infinitamente**: Un propietario puede gestionar cientos de interesados
4. **Disponibilidad 24/7**: Nunca se pierden leads por horarios
5. **Información en tiempo real**: Notificaciones constantes del estado
6. **Calificación automática**: Solo ve perfiles que le interesan
7. **Precios justos**: Avalúo basado en datos reales del mercado

## 🚀 Alcance del MVP

### Geográfico:
- **Ciudad piloto**: Bogotá, Colombia
- **Escalamiento**: Expandir a Colombia completo

### Tipos de Propiedad:
- Casas
- Apartamentos  
- Locales comerciales

### Operaciones:
- Venta
- Arriendo

### Metodología de Avalúo:
- Comparables basados en portales confiables del sector
- Análisis de ubicación, características y precios de mercado
- Sugerencias contextualizadas por zona

## 🎮 Ejemplo de Conversación

```
Propietario: "Hola, quiero arrendar mi apartamento"

Broky: "¡Hola! Soy Broky, tu agente inmobiliario digital. Te ayudaré a arrendar tu apartamento rápidamente. ¿Podrías enviarme la ubicación exacta?"

Propietario: [Envía ubicación - Chapinero Norte]

Broky: "Perfecto, veo que está en Chapinero Norte, excelente zona. ¿Cuántas habitaciones tiene el apartamento?"

Propietario: "2 habitaciones, 2 baños"

Broky: "Genial. ¿Cuántos metros cuadrados aproximadamente?"

[...continúa extrayendo información...]

Broky: "Listo! Basándome en propiedades similares en tu zona, el valor comercial estimado de tu apartamento es $280M-$320M COP. Para arriendo, te sugiero un canon entre $1.8M-$2.2M COP. ¿Te parece bien $2M COP?"

Propietario: "Sí, perfecto"

Broky: "Excelente! Te estoy enviando:
• Afiche PDF para imprimir y poner en tu ventana
• Ficha técnica del apartamento  
• Creativos para que publiques en tus redes

En cuanto alguien escanee el QR del afiche, yo me encargo de todo. Te voy notificando cada interesado para que decidas a quién mostrarle el apartamento."
```

## 🌟 Diferenciadores Clave

1. **WhatsApp Native**: Todo desde una sola aplicación que ya usan
2. **Físico + Digital**: Combina afiche tradicional con tecnología
3. **Avalúo Instantáneo**: Datos reales en segundos
4. **Gestión Ilimitada**: Sin límite de interesados
5. **Calificación Inteligente**: Solo perfiles relevantes
6. **Modelo Freemium**: Valor inmediato sin costo inicial

---

## 📍 Contexto Técnico

### Stack Tecnológico:
- **Mensajería**: Infobip (WhatsApp Business API)
- **Backend**: FastAPI + MongoDB
- **IA**: GPT-4 para conversaciones + Whisper para audio
- **Análisis**: Comparables automáticos con portales inmobiliarios

### Capacidades Core:
- Procesamiento de lenguaje natural en español
- Análisis de imágenes para características de propiedades
- Generación automática de documentos (afiches, fichas)
- Integración con portales para avalúos en tiempo real

---

*Broky: "Lo mejor de la intermediación, sin intermediarios"* 🏠