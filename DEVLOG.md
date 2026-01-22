## 20/01/2026 - Início do projeto e models.py
**O que implementei:**
- startproject setup e startapp menu
- Arquivo dotenv, método load_dotenv() e os.getenv() para proteger e acessar as informações das variáveis DEBUG e SECRET_KEY
- Model Category para as categorias do cardápio
**Desafio:**
- Entender como funciona DEBUG e SECRET_KEY e por quê eu deveria esconder essas variáveis
- Entender qual campo eu utilizo para o nome da categoria
**O que aprendi:**
- DEBUG é o que faz aparecer as mensagens de bug detalhadas no browser e registra todas as queries SQL executadas, o que pode causar mais uso de dados pelo servidor 
- O valor de SECRET_KEY é determinado ao criar um projeto utilizando o comando 'startproject' e o vazamento dele pode permitir um usuário malicioso adicionar mais privilégios a ele, por exemplo
- Choices é um elemento melhor aproveitado em atributos que não mudam. Originalmente, tinha pensado em utilizar esse elemento para as categorias, mas percebi que isso torna o processo de criar ou mudar uma categoria - o que tem altas chances de acontecer - nada dinâmico. Eu precisaria adicionar direto no código (Hard Coded) e ainda utilizar o git pra atualizar. Não gosto.


## 22/01/2026 - Preenchendo o models.py
### Objetivo do dia
Implementar models MenuItem para os itens do cardápio e das categorias, recebendo uma chave estrangeira.
### O que implementei
- Model MenuItem
```python
    class MenuItem(models.Model):

        name = models.CharField(max_length=100, blank=False, null=False)
        category = models.ForeignKey(Category, on_delete=models.CASCADE)
        description = models.TextField(max_length=300, blank=False, null=False)
        price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

        def __str__(self):
            return self.name
```
### Desafios
1. Field Type no atributo price
   - **Problema:** Inicialmente, pensei em usar CharField por conta do 'R$'. Porém, isso não permitiria, futuramente, a possibilidade de calcular o total de um carrinho, já que o dado estaria em texto, ou só atrasaria essa feature. Em seguida, pensei no float, mas ele tem uma precisão desnecessária e, em maior escala, até prejudicial para registrar preços ou até mesmo valores de vendas.
   - **Solução:** Optei por usar DecimalField após fazer algumas pesquisas na documentação oficial do Django e uma breve olhada na documentação do python para a biblioteca 'decimal'. 
   - **O que aprendi:** Descobri durante essas pesquisas que o 'R$' ficaria a cargo do frontend, sendo mais importante para uma apresentação da informação ao usuário e não tanto assim para registrar num banco de dados.
2. Relacionamentos dos dados no banco
    - **Problema:** No começo dos meus estudos, apesar de ter estudado banco de dados mais a fundo e sabendo como os relacionamentos funcionam, me encontrei com certa dificuldade em definir qual seria o modelo de relacionamento mais ideal para esse projeto.
    - **Solução:** Apesar de eu mesmo já ter usado alguns cardápios que permitiam o mesmo cookie em diferentes categorias, eu não gostava porque ficava desorganizado. Optei, então, por manter um relacionamento 1:N entre Categoria e Item do Cardápio, em que um item só poderia fazer parte de uma categoria mas uma categoria pode ter vários itens. Nesse caso, é uma questão de preferência - o que seria uma regra de negócio - para deixar o cardápio final mais organizado.
    - **O que aprendi:** Entendi um pouco melhor como os relacionamentos funcionam.
### Referências
- [Django DecimalField](https://docs.djangoproject.com/en/6.0/ref/models/fields/#decimalfield)
- [Python.org Decimal](https://docs.python.org/3/library/decimal.html)
- [Django Models](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- [Django Relacionamento Many-to-One](https://docs.djangoproject.com/en/6.0/topics/db/examples/many_to_one/)
### Próximos passos
- [ ] Implementar campo de mídia para as fotos dos itens
- [ ] Adicionar configurações de MEDIA