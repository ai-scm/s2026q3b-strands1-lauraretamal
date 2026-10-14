# Agente de viajes con IA para Seattle

Proyecto desarrollado como parte del laboratorio de AWS Skill Builder **Create Advanced AI Agents with Strands SDK and Amazon Bedrock (BETA)**. Utiliza inteligencia artificial generativa para crear un agente de viajes capaz de responder preguntas y ayudar a planificar actividades turísticas en Seattle, Washington.

## ¿Qué hace?

El sistema utiliza el SDK **Strands Agents** y los modelos de Amazon Bedrock para interpretar las solicitudes del usuario y generar respuestas en lenguaje natural.

El agente puede:

- **Consultar el clima:** obtiene información meteorológica mediante una herramienta que consulta los servicios de National Weather Service.
- **Recomendar actividades turísticas:** ofrece información sobre lugares y actividades que se pueden realizar en Seattle.
- **Consultar operadores turísticos:** utiliza información sobre empresas turísticas de la zona para responder preguntas y ayudar a encontrar experiencias de interés.
- **Combinar herramientas:** selecciona las herramientas que necesita según la pregunta y utiliza sus resultados para construir una respuesta.

El objetivo es demostrar cómo un agente de IA puede utilizar herramientas externas y fuentes de información para responder preguntas que van más allá de sus conocimientos internos.

## Tecnologías utilizadas

- **Python:** lenguaje utilizado para implementar la lógica del agente.
- **Strands Agents SDK:** permite crear agentes de IA que interpretan solicitudes y utilizan herramientas.
- **Amazon Bedrock:** proporciona acceso a modelos de inteligencia artificial generativa.
- **AWS SAM:** permite definir y desplegar los recursos necesarios para ejecutar la aplicación en AWS.
- **AWS Lambda:** ejecuta la función que procesa las solicitudes del agente.
- **Amazon CloudFormation:** administra la infraestructura desplegada mediante AWS SAM.

## Requisitos

Antes de utilizar el proyecto, necesitas:

- Una cuenta de AWS con permisos para acceder a Amazon Bedrock y desplegar los recursos requeridos.
- AWS CLI instalado y configurado con las credenciales correspondientes.
- AWS SAM CLI instalado.
- Python y las dependencias indicadas en el proyecto.
- Acceso a un modelo compatible en Amazon Bedrock en la región de AWS seleccionada.

## Instalación y despliegue

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### 2. Verificar las credenciales de AWS

Comprueba que la CLI tenga acceso a tu cuenta:

```bash
aws sts get-caller-identity
```

Asegúrate de utilizar la cuenta y la región en las que tienes los permisos necesarios para desplegar el proyecto.

### 3. Instalar las dependencias

Instala las dependencias de Python:

```bash
pip install -r requirements.txt
```

### 4. Construir la aplicación

Ejecuta el siguiente comando para preparar la aplicación:

```bash
sam build
```

### 5. Desplegar en AWS

Ejecuta:

```bash
sam deploy --guided
```

Sigue las instrucciones para configurar el despliegue, incluyendo la región y los parámetros solicitados. AWS SAM utilizará la plantilla de infraestructura para crear los recursos necesarios.

El despliegue requiere los permisos correspondientes en AWS. Si se produce un error de permisos, revisa los mensajes de la terminal y las políticas asociadas a tu identidad.

## ¿Cómo utilizar el sistema?

Una vez desplegado, el agente puede ejecutarse mediante el mecanismo de invocación configurado en AWS.

Si la función se expone mediante AWS Lambda, puedes probarla desde la consola de Lambda o invocarla con AWS CLI.

Por ejemplo, si la función recibe un evento JSON con el campo `prompt`, puedes utilizar un comando como este:

```bash
aws lambda invoke \
  --function-name NOMBRE_DE_LA_FUNCION \
  --payload '{"prompt":"What are some activities to do in Seattle this weekend?"}' \
  --cli-binary-format raw-in-base64-out \
  response.json
```

Reemplaza `NOMBRE_DE_LA_FUNCION` por el nombre real de la función desplegada. El formato del evento debe coincidir con el que espera la implementación.

Puedes probar solicitudes como:

- `What is the weather forecast for Seattle?`
- `What are some activities to do in Seattle?`
- `Which tour operators offer whale-watching experiences near Seattle?`

El agente interpreta la solicitud, utiliza las herramientas disponibles cuando corresponde y devuelve una respuesta basada en la información obtenida.

## Consideraciones

- Las respuestas dependen de la disponibilidad y actualidad de las fuentes consultadas.
- El uso de Amazon Bedrock y de otros servicios de AWS puede generar costos.
- Las credenciales de AWS y los archivos con información sensible no deben incluirse en el repositorio.
- El proyecto tiene fines educativos y demuestra el funcionamiento de agentes de IA con herramientas integradas en AWS.

## Referencia

Laboratorio de AWS Skill Builder: **Create Advanced AI Agents with Strands SDK and Amazon Bedrock (BETA)**.
```
