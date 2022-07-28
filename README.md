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
		"rules": str

    }
```
donde:
- Task: string con la tarea a ejecutar: CANCELLATION, CHANGE, etc
- Information: string de la información del ticket: fareBasis, origin, date departure, etc
- Rules: string de la clase con las reglas correspondiente, por ejemplo para cancelación es la clase 16.

por ejemplo

```json
    {
        "task": "CANCELLATION",
		"information": "Ticket Information:\n fareBasis = H13USR3APO/CH25\n airLine = SQ \n departureDate = 2022-11-05T21:15:00\n route = origin: JFK\n destination: FRA \nticketNumber: 6185860002240\n ticketIssuanceDate: 2022-05-31T00:00:00+00:00\n reservationDate: 2022-05-05T21:15:00\n cancelationDate: 2022-05-10T02:15:00\n",
		"rules" :"CANCELLATIONS\nANY TIME\nCHARGE USD 200.00 FOR CANCEL.\nNOTE - TEXT BELOW NOT VALIDATED FOR AUTOPRICING.

    }
```

el modelo GPT responderá:
- question: pregunta que se realiza acerca de las reglas entregadas.

- quote: parrafo o texto de donde extrajo la respuesta.
- answer: respuesta del modelo
- boolean: para indicar con True o False si el modelo encontró una respuesta.

Por ejemplo: 

```json
   {
	"question_1": {
		"answer": "CANCELLATIONS PERMITTED FOR REFUND.",
		"quote": "ANY TIME\\nCHARGE USD 200.00 FOR CANCEL.\\nNOTE  TEXT BELOW NOT VALIDATED FOR AUTOPRICING.",
		"boolean": true,
		"question": "The text says that the CANCELLATIONS is?"
	},
	"question_2": {
		"answer": "ANY TIME.",
		"quote": "ANY TIME\\nCHARGE USD 200.00 FOR CANCEL.\\nNOTE  TEXT BELOW NOT VALIDATED FOR AUTOPRICING.",
		"boolean": true,
		"question": "According to the rules at which time you can cancel"
	},
	"question_3": {
		"answer": "USD 200.00",
		"quote": "CHARGE USD 200.00 FOR CANCEL.",
		"boolean": true,
		"question": "How much is the CHARGE FOR CANCEL?",
		"value": 200.0,
		"denomination": "USD"
	},
	"question_4": {
		"answer": "2022-11-05T211500",
		"quote": "fareBasis = H13USR3APO/CH25\\nairLine = SQ \\ndepartureDate = 2022-11-05T211500\\nroute = origin JFK\\ndestination FRA \\nticketNumber 6185860002240\\nticketIssuanceDate 2022-05-31T000000+0000\\nreservationDate 2022-05-05T211500\\ncancelationDate 2022-05-10T021500",
		"boolean": false,
		"question": "What is the departure date?"
	},
	"question_5": {
		"answer": "refundable",
		"quote": "CANCELLATIONS PERMITTED FOR REFUND.\\nCHARGE USD 200.00 FOR CANCEL.",
		"boolean": true,
		"question": "According to the above, is the ticket refundable?"
	}
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

* **Wilberth Ferney Córdoba Canchala** - *Trabajo Inicial* - [LinkenId](https://github.com/villanuevand)
## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* etc.