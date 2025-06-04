# Project Description

This project is an AI enabled restaurant review summarizer pipeline. The goal of this is to build a real-time prompt-engineered local application utilizing different options of LLM -- the API enabled GPT option, and an on-premise llama-2. Utilizing **FAISS** as well as **langchain**, the project aims to provide a context-aware summarizer, where based on real-time retrieved reviews, the application can quickly return users summarized reviews about different features that they might be curious about from a restaurant of interest, such as price, service, food quality, or anything!

The project provides support for both chatGPT and llama2. There are LLM declaration files, such as _llm_chain.py_ that allow users to switch between the options. The code also provides the options to download quantized version of llama2. There's also script provided such that, if user doesn't already have a ready on-prem LLM, they can run the script and download the llama2 from huggingface.

## Interactions

There are three stages involved within the project: retrieval, processing, and output.

The retrieval process is done by interacting with a front end interface, where users are prompted to enter a restaurant name. A request is then made to the backend, where in real-time a list of search results about the restaruant would be returned, achieved by using **Google Places API**. After the restaurnat is selected, the user would then be able to load reviews associated with the restaurant.

The next step would then be index the retrieved reviews into a **FAISS index**.

After reviews are loaded into index, the user is prompted to select a feature they are curious about from the restaurant. They can either select existing feature, or enter information on a custom field. Then, a request containing the asked feature is sent to the backend, where, using FAISS indexing, the feature would invoke searching within the index, and then the index will pull the most relevant reviews related to the feature to use as context. T

Continueing the process, the reviews are then passed to a summarizing step, where the LLM, taking prompt engineered instructions, summarize the reviews and answer about the asked feature.

Finally, the ouput is returned to the user, displayed in the frontend.

# Setup and Installations

## APIs

To set up, the user needs to first obtain API keys from [OpenAI](https://openai.com/index/openai-api/) and [Google places API](https://developers.google.com/maps/documentation/places/web-service/get-api-key?_gl=1*1ipqrma*_up*MQ..*_ga*OTM1Mzg5NTM5LjE3NDgxMTkxMzY.*_ga_NRWSTWS78N*czE3NDgxMTkxMzUkbzEkZzEkdDE3NDgxMTkxOTckajAkbDAkaDA.). For google places, the user may also need to [set up a project](https://developers.google.com/maps/documentation/places/web-service/cloud-setup?_gl=1*18wnwwe*_up*MQ..*_ga*OTM1Mzg5NTM5LjE3NDgxMTkxMzY.*_ga_NRWSTWS78N*czE3NDgxMTkxMzUkbzEkZzEkdDE3NDgxMTkyMjYkajAkbDAkaDA.).

_optional_
If the user wants to use on-prem LLM, they can obtain login code from [hugging face](https://huggingface.co/settings/tokens). If they want to request llama2, they would also need to make a request to meta via hugging face, [here](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf).

## Installations and running

After following the instructions from **Frontend** and **Backend**, the application should be good to go.

### Frontend

Just run

```bash
npm run dev
```

This will begin the frontend server. The frontend folder contains a _.env.local_ file that points to the backend server at http://localhost:8000.

### Backend

You can either manually create a virtual environment following the instructions from manual installations, or, if you have docker, go straight to the **Docker** session further down in the page.

#### Manual Installation

You would need [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html) for this.

Run:

```bash
conda create -n places-env python=3.12
conda activate places-env
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

This would start the backend server too.

##### Environmental variables

If you are using **manual installation**, you would need to define a _.env_ file in _/backend_ folder. The _.env_ file can look like this:

```bash
GOOGLE_MAPS_API_KEY={GOOGLE_MAPS_API_KEY}
OPENAI_API_KEY={OPENAI_API_KEY}
HUGGING_FACE_TOKEN={HUGGING_FACE_TOKEN}
```

#### Docker

If there's docker pre-installed, navigate to the _/backend_ folder, and run

```bash
docker build -t ecom-review-backend:latest .
```

Then
docker run -d \
 --name review-api \
 -p 8000:8000 \
 -e GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY} \
  -e OPENAI_API_KEY=${OPENAI_API_KEY} \
 ecom-review-backend:latest

## On-premise LLM option

Run

```bash
python load_local_llm.py
```

within _load_local_llm.py_, there's also optional flag to enable 8-bit quantized model. You can enable it if you wish to download it, but it may require _bitsandbytes_ package, in which case, you may have to run

```bash
pip install bitsandbytes
```

Then, you can start following the instructions in llm_chain to replace the llm model from ChatGPT to the installed llama2.
