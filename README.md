<a id="readme-top"></a>

<!-- HEADER -->
# Concept Map Generator

<!-- TABLE OF CONTENT -->
<details>
  <summary>Table of content</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#backend">Backend</a></li>
        <li><a href="#frontend">Frontend</a></li>
      </ul>
    </li>
    <li>
      <a href="#">Features</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li>
      <a href="#references">References</a>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

A **Concept Map** is a tool for visualizing relationships between concepts and ideas. A **Concept Map Generator** uses Natural Language Processing (NLP) to identify concepts, resolve references, and form triples (concept → relation → concept) that can be used to build a concept map.

The goal of this project is to extract concept maps from the abstracts of research papers. This results in a graphical summarization of the text, which can be easier to comprehend.

This application can be used to extract a concept map from any short text, not just abstracts. However, it also provides the option to upload an entire paper in PDF format to improve the results.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BACKEND -->
### Backend

The backend is built with the following technologies:

* [![Python][Python-badge]][Python-url]
* [![Flask][Flask-badge]][Flask-url]
* [![spaCy][spaCy-badge]][spaCy-url]
* [![NeuralCoref][NeuralCoref-badge]][NeuralCoref-url]
* [![NetworkX][NetworkX-badge]][NetworkX-url]
* [![nltk][nltk-badge]][nltk-url]
* [![scikit-learn][scikit-learn-badge]][scikit-learn-url]

The backend uses **Flask** to serve APIs for processing text input and PDF files. It performs NLP tasks like tokenization, dependency parsing, and coreference resolution using **spaCy** and **NeuralCoref**. It also constructs a graph of concept relationships using **NetworkX**.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FRONTEND -->
### Frontend

The frontend is built with the following technologies:

* [![JavaScript][JavaScript-badge]][JavaScript-url]
* [![React][React-badge]][React-url]
* [![Material-UI][Material-UI-badge]][Material-UI-url]
* [![React Flow][React-Flow-badge]][React-Flow-url]

The frontend is built using **React**, a JavaScript library for building user interfaces. **Material-UI** is used to create a modern and responsive design. **React Flow** is integrated for rendering the concept map graph with interactive nodes and edges.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FEATURES -->
## Features

- 📄 Upload PDF or input raw text
- 🧠 NLP pipeline with coreference resolution
- 🧭 Extracts and visualizes concept relationships
- 🌐 Interactive concept map with React Flow

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This section will help you set up the project locally for development and testing purposes. Follow the steps for both the backend (Python/Flask) and the frontend (React).

<!-- PREREQUISITES -->
### Prerequisites

Before you begin, make sure you have the following:

#### Backend
- Python 3.7.0 (or any other version of Python 3)
- pip (Python package installer)

#### Frontend
- Node.js
- npm or yarn

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Installation -->
### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/AlexBadita/concept-map-generator.git
cd concept-map-generator
```

#### 2. Install the Backend Dependencies

Navigate to the backend folder from the terminal:
```bash
cd flask-backend
```

Run the script to create a local virtual environment (because the app requires Python 3.7.0 and some specific versions for some dependencies). <br/>
The full list of required dependencies can be found in *requirements.txt*. <br/>
**Before running the script make sure you know which shell you’re using** (zsh, bash, etc.). Check the *init_venv.sh* before running it.
```bash
 ./init_venv.sh
```

#### 3. Run the Backend Server

Optional: If your local environment is not activated in your terminal, run:
```bash
source .venv/bin/activate
```

Once your virtual environment is activated, you can start the flask server:
```bash
python3 backend.py
```

#### 4. Install the Frontend Dependencies

In a new terminal, navigate to the frontend folder:
```bash
cd concept-map
```

Then, install the dependencies:
```bash
npm install
```

#### 5. Start the Client Application
```bash
npm start
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- REFERENCES -->
## References

1. **Automatic Structured Text Summarization with Concept Maps**
   *Author: Tobias Falke, 2019*
   [Link to paper](https://tuprints.ulb.tu-darmstadt.de/8430/1/PhDThesis_TobiasFalke.pdf)
   
2. **Semi-Automatic Creation of Concept Maps**
   *Author: Christoph Presch, 2020*
   [Link to paper](https://www.cg.tuwien.ac.at/research/publications/2020/Presch_2020/Presch_2020-Master%20Thesis.pdf)

3. **Concept Map Mining as Browser Extension**
   *Author: Mario Stoff, 2021*
   [Link to paper](https://www.cg.tuwien.ac.at/research/publications/2021/stoff-concepMap-2021/stoff-concepMap-2021-thesis.pdf)

4. **Automatic Construction Of Concept Maps From Texts**
   *Author: Camila Zacché de Aguiar, Amal Zouaq, Davidson Cury, 2016*
   [Link to paper](https://www.researchgate.net/publication/311424610_AUTOMATIC_CONSTRUCTION_OF_CONCEPT_MAPS_FROM_TEXTS)

5. **Using Automatically Generated Concept Maps for Document Understanding: a Human Subjects Experiment**
   *Author: Alejandro Valerio, David B. Leake, 2012*
   [Link to paper](https://www.researchgate.net/publication/320809098_Using_Automatically_Generated_Concept_Maps_for_Document_Understanding_a_Human_Subjects_Experiment)

6. **Associating Documents To Concept Maps In Ccontext**
   *Author: Alejandro Valerio, David B. Leake, 2008*
   [Link to paper](https://www.researchgate.net/profile/Alejandro-Valerio/publication/255549752_ASSOCIATING_DOCUMENTS_TO_CONCEPT_MAPS_IN_CONTEXT/links/02e7e5350173920a2d000000/ASSOCIATING-DOCUMENTS-TO-CONCEPT-MAPS-IN-CONTEXT.pdf)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Python-badge]: https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/

[Flask-badge]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/

[spaCy-badge]: https://img.shields.io/badge/spaCy-09A3D5?style=for-the-badge
[spaCy-url]: https://spacy.io/

[NeuralCoref-badge]: https://img.shields.io/badge/NeuralCoref-FF6F61?style=for-the-badge
[NeuralCoref-url]: https://github.com/huggingface/neuralcoref

[NetworkX-badge]: https://img.shields.io/badge/NetworkX-1E4E79?style=for-the-badge
[NetworkX-url]: https://networkx.org/

[JavaScript-badge]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://www.javascript.com/

[React-badge]: https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black
[React-url]: https://reactjs.org/

[Material-UI-badge]: https://img.shields.io/badge/Material--UI-007FFF?style=for-the-badge&logo=material-ui&logoColor=white
[Material-UI-url]: https://mui.com/

[React-Flow-badge]: https://img.shields.io/badge/React%20Flow-00D1B2?style=for-the-badge&logo=react&logoColor=white
[React-Flow-url]: https://reactflow.dev/

[nltk-badge]: https://img.shields.io/badge/nltk-85C1E9?style=for-the-badge
[nltk-url]: https://www.nltk.org/

[scikit-learn-badge]: https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white
[scikit-learn-url]: https://scikit-learn.org/
