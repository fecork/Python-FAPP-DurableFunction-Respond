# Reading Comprehension con GPT Para lectura de Fare Rules

Código para Leer texto de Fare Rules de TPTravel, y responder si es posible una cancelación y si es reembolsable. 


## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.


### Pre-requisitos 📋

Instalar
- [Azure Function Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash)
- [Extensión Azure Function para Visual Studio](https://github.com/microsoft/vscode-azurefunctions)

### Instalación 🔧




Para ejecutar en local

```
pip install -r requirements.txt
```

En Azure las librerías se instalan automaticamente

## Ejecutando ⚙️

```
func host start
```

## API 🦉

consultar al modelo por la ruta

```
https://tptravel-model.azurewebsites.net/api/GptModelPoliciesTpt?
```

Recibe el objeto Json

```json
    {
        "task": str,
		"information": str,
		"penaltyText": [objects]

    }
```
donde:
- Task: string con la tarea a ejecutar: CANCELLATION, CHANGE, etc
- Information: string de la información del ticket: fareBasis, origin, date departure, etc
- Rules: string de la clase con las reglas correspondiente, por ejemplo para cancelación es la clase 16.

por ejemplo

```json
"penaltyText":[
    {
      "fareBasis": "KLEQPZ0K",
      "categories": [
        {
          "code": "16",
          "freeText": "CHANGES\nANY TIME\nCHANGES NOT PERMITTED IN CASE OF REISSUE/\nREVALIDATION.\nANY TIME\nCHANGES NOT PERMITTED IN CASE OF NO-SHOW.\nNOTE"
		  "name":"Penalties"
		}
		{
		 "code":"19",
		 "freeText":
		 "name":
		}
```

el modelo GPT responderá:
- question: pregunta que se realiza acerca de las reglas entregadas.
- quote: parrafo o texto de donde extrajo la respuesta.
- answer: respuesta del modelo
- boolean: para indicar con True o False si el modelo encontró una respuesta.
- category: para indicar de que categoría extrajo la respuesta
- meanProbability: indica la probabilidad media de generación de cada token en la respuesta

Por ejemplo: 

```json
   {
				"question": "\"1. According to the rules at which time you can cancel\"",
				"answer": "You can cancel at ANY TIME.",
				"category": 16,
				"quote": "ANY TIME. TICKET IS NONREFUNDABLE.",
				"numberQuestion": 1,
				"boolean": true,
				"meanProbability": 97.75423896420118
			},
			{
				"question": "\n\"2. How much is the CHARGE FOR CANCEL?\"",
				"answer": "The charge for cancel is the sum of the cancellation fees of all cancelled fare components.",
				"category": 16,
				"quote": "WHEN COMBINING REFUNDABLE FARES WITH NON REFUNDABLE FARES PROVISIONS WILL APPLY AS FOLLOWS THE AMOUNT PAID ON THE REFUNDABLE FARE COMPONENT WILL BE REFUNDED UPON PAYMENT OF THE PENALTY AMOUNT IF APPLICABLE. THE AMOUNT PAID ON THE NON-REFUNDABLE FARE COMPONENT WILL NOT BE REFUNDED. WHEN COMBINING FARES CHARGE THE SUM OF THE CANCELLATION FEES OF ALL CANCELLED FARE COMPONENTS.",
				"numberQuestion": 2,
				"boolean": true,
				"meanProbability": 97.75423896420118,
				"value": null,
				"denomination": "The charge for cancel is the sum of the cancellation fees of all cancelled fare components."
			},
			{
				"question": "\n\"3. What is the departure date?\"\n",
				"answer": "The departure date is November 5th 2022 at 2115.",
				"category": 16,
				"quote": "Ticket Information fareBasis = H13USR3APO/CH25 airLine = SQ departureDate = 2022-11-05T211500 route = origin JFK destination FRA ticketNumber 6185860002240 ticketIssuanceDate 2022-05-31T000000+0000 reservationDate 2022-05-05T211500 cancelationDate 2022-05-10T021500",
				"numberQuestion": 3,
				"boolean": true,
				"meanProbability": 97.75423896420118
			},
			{
				"question": "4. Is refundable?",
				"answer": "NonRefundable",
				"category": 16,
				"quote": "",
				"numberQuestion": 4,
				"boolean": false,
				"meanProbability": 82.63212880372367
			},
			{
				"question": "5. List all the charges shown in the text",
				"answer": [
					"100 percent of the fare for accompanied children 2-11 no discount for infants with a seat under 2 10 percent of the fare for first infants without a seat under 2 100 percent of the fare for unaccompanied children 8-11"
				],
				"category": 19,
				"quote": [
					"CNNACCOMPANIED CHILD PSGR 2-11 - CHARGE 100 PERCENT OF THE FARE.",
					"OR - INSINFANT WITH A SEAT PSGR UNDER 2 - NO DISCOUNT.",
					"OR - 1ST INFINFANT WITHOUT A SEAT PSGR UNDER 2 - CHARGE 10 PERCENT OF THE FARE.",
					"OR - UNNUNACCOMPANIED CHILD PSGR 8-11 - CHARGE 100 PERCENT OF THE FARE."
				],
				"numberQuestion": 5,
				"boolean": true,
				"meanProbability": 95.83486723862995
			}
```

para la question_3 se entrega además:

- value: valor flotante con el cargo encontrado
- denomination: moneda o denominación del cargo: USD, JPY, GBP

por ejemplo.

```json
	"question_3": {
		"answer": "USD 200.00",
		"quote": "CHARGE USD 200.00 FOR CANCEL.",
		"boolean": true,
		"question": "How much is the CHARGE FOR CANCEL?",
		"value": 200.0,
		"denomination": "USD"
	},
```




## Despliegue 📦

El código se encuentra desplegado en la Azure Function.

```
tptravel-model
```

del grupo de recursos

```
TPTravelDEV12901
```

de la suscripción

```
Teleperformance Colombia
```

Los guías usadas para desplegar son:

[Visual Studio Code](https://fecork.notion.site/Desplegar-c-digo-en-Azure-Function-con-Visual-Studio-Code-df55f8a586af43709ef499ab4dc298c4)

[Pipeline](https://fecork.notion.site/Pipeline-para-Azure-Function-4a46b6b2529a4311841d6a51516ecf2a)

[Release](https://fecork.notion.site/Release-para-Azure-Function-3203b3a312aa40a79c2074533fc252d5)

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Azure Functions SDK](https://pypi.org/project/azure-functions/) - Microsoft
* [OpenAI API](https://openai.com/blog/openai-api/) - Modelo GPT3
* [Spacy](https://spacy.io) - Librería para procesar texto

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Autores ✒️

_Menciona a todos aquellos que ayudaron a levantar el proyecto desde sus inicios_

* **Wilberth Ferney Córdoba Canchala** - *Trabajo Inicial* - [LinkenId](https://www.linkedin.com/in/wilberth-ferney-córdoba-canchala-9734b74b/)
## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* etc.