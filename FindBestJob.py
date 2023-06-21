"""
The code starts by importing the necessary libraries and modules, including pandas, torch, numpy,
cosine_similarity from sklearn, and the BertTokenizer and BertModel from the transformers library.
"""


"""
AI is used in the code in the following ways:

1. BERT Model: The code utilizes the BERT (Bidirectional Encoder Representations from Transformers) model, which is a state-of-the-art transformer-based model for natural language understanding. BERT has been pre-trained on a large corpus of text data and has learned to understand the context and meaning of words and sentences.
2. BERT Tokenizer: The BERT tokenizer is employed to tokenize the user input and job descriptions. Tokenization is the process of breaking text into individual tokens or words. The tokenizer handles splitting words, adding special tokens, and converting text into numerical representations (input IDs) that can be understood by the BERT model.
3. BERT Embeddings: The BERT model is used to generate embeddings for both the user input and job descriptions. Embeddings are dense vector representations that capture the semantic meaning and context of the input. BERT embeddings encode the contextual information, allowing the model to understand the relationships between words and phrases in the input.
4. Cosine Similarity: The code utilizes cosine similarity, a mathematical metric, to measure the similarity between the user's input embedding and the embeddings of each job description. Cosine similarity measures the cosine of the angle between two vectors and provides a similarity score ranging from -1 to 1. A higher cosine similarity score indicates a higher similarity between two vectors.
5. Machine Learning: Although the code does not involve training the model in this specific scenario, the BERT model itself is a result of machine learning. BERT has been trained on a large amount of text data using unsupervised learning techniques to capture language patterns and semantics. By using the pre-trained BERT model, the code benefits from the learned representations and semantic understanding of the language.

By leveraging the power of the BERT model and cosine similarity, the code applies AI techniques to understand the user's input, encode it into meaningful representations, and compare it with job descriptions to find the best job option based on similarity.


Why we choose to use BERT ?
BERT (Bidirectional Encoder Representations from Transformers) is chosen for this case because it offers several benefits for natural language processing tasks like job recommendation:

1. Contextual Understanding: BERT has been pre-trained on a large amount of text data using a masked language modeling objective. This pre-training enables BERT to capture contextual understanding of words and sentences. It understands the meaning and context of words based on their surrounding words, allowing it to generate rich and meaningful representations for text inputs.
2. Semantic Similarity: BERT embeddings encode semantic information, meaning they capture the relationships between words and phrases. By using BERT embeddings, we can measure the similarity between the user's input and job descriptions in a meaningful way. This enables us to find jobs that are closely related to the user's preferences, even if they use different words or phrases.
3. Transfer Learning: BERT is a pre-trained model, which means it has already learned useful language representations from a large corpus of data. By utilizing this pre-trained model, we can benefit from its knowledge and understanding of language without the need to train a language model from scratch. This saves significant computational resources and time.
5. State-of-the-Art Performance: BERT has achieved state-of-the-art performance on various natural language processing tasks. It has demonstrated its effectiveness in understanding and representing language semantics, making it a powerful choice for tasks that require understanding and matching user preferences with job descriptions.

Overall, BERT is chosen in this case because it provides contextual understanding, semantic similarity, transfer learning benefits, fine-tuning flexibility, and state-of-the-art performance. These qualities make BERT well-suited for job recommendation tasks where understanding the user's preferences and matching them with relevant job descriptions is crucial.
"""




import pandas as pd
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel # type: ignore
import nlp
def find_the_best_job(df_QA, job_data):
    # df_QA = create_demo_user()
    # jobs_df = create_demo_job_list()
    jobs_df = pd.DataFrame(job_data)
    print(jobs_df)
    # Load the BERT tokenizer and model
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    for index, row in df_QA.iterrows():
        # Access the values in each row
        # The user's answers are combined into a single input string, user_input, using whitespace as a separator.
        user_input = row['Combined_Answers']

        """
        The user input is tokenized and encoded using the BERT tokenizer. 
        The encode_plus() method converts the user input into input IDs and attention masks, 
        which are required inputs for the BERT model. 
        The input IDs represent the tokenized text, and the attention mask helps the model focus on 
        relevant parts of the input.
        """
        encoded_dict = tokenizer.encode_plus(
            user_input,
            add_special_tokens=True,
            max_length=512,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        input_ids = encoded_dict['input_ids']
        attention_mask = encoded_dict['attention_mask']

        # Set the device for BERT model - The device for running the BERT model is set to either GPU (if available) or CPU.
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # The BERT model is moved to the chosen device using model.to(device). The input IDs and attention masks are also moved to the same device.
        model.to(device)
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)

        # Obtain the BERT embeddings for the user input
        """
        disables gradient computation. 
        This means that during the execution of the block of code within the context manager, 
        PyTorch won't track operations for computing gradients. 
        This is useful for inference or evaluation where we don't need to update model parameters (i.e. train the mdoel)
        """
        with torch.no_grad():
            """
            passes the input tensors input_ids and attention_mask to the BERT model. 
            The model takes the input IDs that represent the tokenized text and the attention mask that helps the model
            focus on relevant parts of the input. It then performs forward propagation and returns the outputs.
            """
            outputs = model(input_ids, attention_mask)

            """
            Extracts the BERT embeddings from the outputs. The embeddings are stored in the first element of the tuple, 
            The indexing [:, 0, :] selects all rows, the first column, and all elements in the last dimension 
            (which represents the embedding dimensions). Finally, .cpu().numpy() converts the tensor to a NumPy array 
            for further processing.
            """
            user_embedding = outputs[0][:, 0, :].cpu().numpy()

        # Compute the similarity between the user input and each job description
        job_embeddings = []

        for _, job_row in jobs_df.iterrows():
            encoded_dict = tokenizer.encode_plus(
                job_row['job_description'],
                add_special_tokens=True,
                max_length=512,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            input_ids = encoded_dict['input_ids']
            attention_mask = encoded_dict['attention_mask']

            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)

            with torch.no_grad():
                outputs = model(input_ids, attention_mask)
                job_embedding = outputs[0][:, 0, :].cpu().numpy()
                # job_embeddings.append(job_embedding)
                job_embeddings.append(torch.tensor(
                    job_embedding))  # Convert to tensor

        job_embeddings = torch.cat(job_embeddings, dim=0)

        # Calculate cosine similarity between user input and job descriptions
        similarity_scores = cosine_similarity(user_embedding, job_embeddings)

        # Find the index of the most similar job
        best_job_index = similarity_scores.argmax()

        # Get the details of the best job option from the jobs
        best_job = jobs_df.iloc[best_job_index]

        short_description = nlp.get_short_description(
            best_job['job_description'])

        new_offer = "Job Name: {}<br>Company: {}<br>Description: {}<br>".format(best_job['job_name'],
                                                                                best_job['company_name'],
                                                                                short_description)
        return new_offer
