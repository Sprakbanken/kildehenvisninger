import spacy
import prodigy
import srsly

from prodigy import get_stream
from prodigy.components.preprocess import add_tokens

from scripts.regex_spans import regex_span_finder
#from scripts.task_router import custom_task_router


@prodigy.recipe(
    "span-recipe",
    dataset=("The dataset to save answers to", "positional", None, str),
    source=("The source data with examples to annotate", "positional", None, str),
    label=("One or more comma-separated labels", "option", "l", str),
    model=("The base model", "option", "m", str),
    patterns=("Optional match patterns", "option", "p", str),
)
def citation_span_recipe(dataset, source, label, model="nb_core_news_sm", patterns=None):

    def add_spans(nlp, stream):

        for ex in stream:
            doc = nlp(ex["text"])
            ex["spans"] = doc.spans["regex"] + doc.spans["sc"]
            yield ex

    nlp = spacy.load(model)
    nlp.add_pipe("regex_span_finder", after="ner")

    if patterns is not None:
        loaded_patterns = srsly.read_jsonl(patterns)
        ruler = nlp.add_pipe("span_ruler", config=dict(spans_key="sc"), after="regex_span_finder")
        ruler.add_patterns(loaded_patterns)

    stream = get_stream(source, rehash=True)
    stream = add_spans(nlp, stream)
    stream = add_tokens(nlp, stream)

    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": "spans_manual",
    #    "task_router": custom_task_router,
    }


example = {
    "text":"Sp\u00f8rsm\u00e5let om hvorvidt det finnes noen regler for tilordning av genus i norsk er et tema som har v\u00e6rt mye diskutert opp gjennom \u00e5rene (se for eksempel Trosterud 2001), og bidraget fra Urek, Lohndal og Westergaard (2022) tar opp nettopp dette problemet.",
    "_input_hash":-343350999,
    "_task_hash":1923224411,
    "tokens":[
        {
            "text":"Sp\u00f8rsm\u00e5let",
            "start":0,
            "end":10,
            "id":0,
            "ws":true
        },
        {"text":"om","start":11,"end":13,"id":1,"ws":true},
        {"text":"hvorvidt","start":14,"end":22,"id":2,"ws":true},
        {"text":"det","start":23,"end":26,"id":3,"ws":true},
        {"text":"finnes","start":27,"end":33,"id":4,"ws":true},
        {"text":"noen","start":34,"end":38,"id":5,"ws":true},
        {"text":"regler","start":39,"end":45,"id":6,"ws":true},
        {"text":"for","start":46,"end":49,"id":7,"ws":true},
        {"text":"tilordning","start":50,"end":60,"id":8,"ws":true},
        {"text":"av","start":61,"end":63,"id":9,"ws":true},
        {"text":"genus","start":64,"end":69,"id":10,"ws":true},
        {"text":"i","start":70,"end":71,"id":11,"ws":true},
        {"text":"norsk","start":72,"end":77,"id":12,"ws":true},
        {"text":"er","start":78,"end":80,"id":13,"ws":true},
        {"text":"et","start":81,"end":83,"id":14,"ws":true},
        {"text":"tema","start":84,"end":88,"id":15,"ws":true},
        {"text":"som","start":89,"end":92,"id":16,"ws":true},
        {"text":"har","start":93,"end":96,"id":17,"ws":true},
        {"text":"v\u00e6rt","start":97,"end":101,"id":18,"ws":true},
        {"text":"mye","start":102,"end":105,"id":19,"ws":true},
        {"text":"diskutert","start":106,"end":115,"id":20,"ws":true},
        {"text":"opp","start":116,"end":119,"id":21,"ws":true},
        {"text":"gjennom","start":120,"end":127,"id":22,"ws":true},
        {"text":"\u00e5rene","start":128,"end":133,"id":23,"ws":true},
        {"text":"(","start":134,"end":135,"id":24,"ws":false},
        {"text":"se","start":135,"end":137,"id":25,"ws":true},
        {"text":"for","start":138,"end":141,"id":26,"ws":true},
        {"text":"eksempel","start":142,"end":150,"id":27,"ws":true},
        {"text":"Trosterud","start":151,"end":160,"id":28,"ws":true},
        {"text":"2001","start":161,"end":165,"id":29,"ws":false},
        {"text":")","start":165,"end":166,"id":30,"ws":false},
        {"text":",","start":166,"end":167,"id":31,"ws":true},
        {"text":"og","start":168,"end":170,"id":32,"ws":true},
        {"text":"bidraget","start":171,"end":179,"id":33,"ws":true},
        {"text":"fra","start":180,"end":183,"id":34,"ws":true},
        {"text":"Urek","start":184,"end":188,"id":35,"ws":false},
        {"text":",","start":188,"end":189,"id":36,"ws":true},
        {"text":"Lohndal","start":190,"end":197,"id":37,"ws":true},
        {"text":"og","start":198,"end":200,"id":38,"ws":true},
        {"text":"Westergaard","start":201,"end":212,"id":39,"ws":true},
        {"text":"(","start":213,"end":214,"id":40,"ws":false},
        {"text":"2022","start":214,"end":218,"id":41,"ws":false},
        {"text":")","start":218,"end":219,"id":42,"ws":true},
        {"text":"tar","start":220,"end":223,"id":43,"ws":true},
        {"text":"opp","start":224,"end":227,"id":44,"ws":true},
        {"text":"nettopp","start":228,"end":235,"id":45,"ws":true},
        {"text":"dette","start":236,"end":241,"id":46,"ws":true},
        {"text":"problemet","start":242,"end":251,"id":47,"ws":false},
        {"text":".","start":251,"end":252,"id":48,"ws":false}
    ],
    "_view_id":"spans_manual",
    "spans":[
        {"start":151,"end":165,"token_start":28,"token_end":29,"label":"REF"},
        {"start":184,"end":219,"token_start":35,"token_end":42,"label":"REF"}],
    "answer":"accept",
    "_timestamp":1690289516,
    "_annotator_id":"2023-07-25_14-50-21",
    "_session_id":"2023-07-25_14-50-21"
    }
