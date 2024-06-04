#!/usr/bin/env python
# coding: utf-8

# In[1]:


from s2ag_corpus.database_catalogue import DatabaseCatalogue, production_connection
from s2ag_corpus.dot_writer import write_dot_file


# In[2]:


connection = production_connection()
catalogue = DatabaseCatalogue(connection)


# In[3]:


id = catalogue.find_corpus_id_from('4747e72c5bc706c50e76953188f0144df18992d0')


# In[4]:


catalogue.find_paper_details(id)


# In[5]:


# connection.rollback()


# In[13]:


enriched_links = catalogue.enriched_links(id)


# In[7]:


write_dot_file(enriched_links, 'code-gen.dot')


# In[ ]:


# get_ipython().system('dot -Tsvg code-gen.dot -o code-gen.svg')

