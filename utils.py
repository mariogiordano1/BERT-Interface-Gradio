import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from transformers import pipeline
import mysql.connector


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
MODEL_PATH = 'mariogiordano/Bert-emotion-analysis'

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model = model.to(DEVICE)


def get_predictions(input_text= str) -> dict:
    #label2id = model.config.label2id
    inputs = tokenizer(input_text, return_tensors='pt', truncation=True)
    inputs = inputs.to(DEVICE)
    outputs = model(**inputs)
    logits = outputs.logits
    labels = get_labels(input_text)
    labels = [label.replace('LABEL_0','Gioia') for label in labels]
    labels = [label.replace('LABEL_1','Tristezza') for label in labels]
    labels = [label.replace('LABEL_2','Rabbia') for label in labels]
    labels = [label.replace('LABEL_3','Paura') for label in labels]
    labels = [label.replace('LABEL_4','Vergogna') for label in labels]
    labels = [label.replace('LABEL_5','Disgusto') for label in labels]
    labels = [label.replace('LABEL_6','Colpevolezza') for label in labels]
    probs = get_scores(input_text)
    #sigmoid = torch.nn.Sigmoid()
    #probs = sigmoid(logits.squeeze().cpu())    
    #for i, k in enumerate(label2id.keys()):
    #    label2id[k] = probs[i]
    res = {}
    for lab in labels:
        for value in probs:
            res[lab] = value
            probs.remove(value)
            break
        
    return(res)


def get_scores(text):
    classifier = pipeline("text-classification", model="mariogiordano/Bert-emotion-analysis")
    pred = classifier([text], top_k=None)
    i = 0
    count = 0
    scores = []
    for i in range(len(pred[0])):
        for line in pred:
            #print(line[i]['score'])
            scores.append(line[i]['score'])
    return scores
        
        
def get_labels(text):
    classifier = pipeline("text-classification", model="mariogiordano/Bert-emotion-analysis")
    pred = classifier([text], top_k=None)
    i = 0
    count = 0
    labels = []
    for i in range(len(pred[0])):
        for line in pred:
            #print(line[i]['score'])
            labels.append(line[i]['label'])
    return labels

def save_correction(input_text=str, empred=str, new_emotion=str):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0000",
    database="frasi_corrette"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO dataset (frase, emozione_predetta, emozione_corretta) VALUES (%s, %s, %s)"
    val = (input_text, empred, new_emotion)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    
    
def get_first_key(input_text=str):
    results = get_predictions(input_text)
    first = list(results.keys())[0]
    return first