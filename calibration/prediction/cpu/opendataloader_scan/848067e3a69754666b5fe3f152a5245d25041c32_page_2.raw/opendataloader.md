# 2.2 Controle por avan¸o e/ou atraso de fase usando LGR

Discretize a fun¸c˜ao de transferˆencia (1). O objetivo ´e projetar um sistema de controle de posi¸c˜ao de modo que requisitos como sobressinal e instante de pico sejam atendidos. O erro estaciona´rio deve ser nulo para entrada degrau (e onda quadrada). O controlador deve ser do tipo avan¸co e/ou atraso de fase. O projeto deve ser feito utilizando o m´etodo do lugar geom´etrico das ra´ızes. O per´ıodo de amostragem deve ser compat´ıvel com a planta e com os requisitos de projeto escolhidos. Utilize um limitador de tens˜ ao no Simulink na sa´ıda do controlador (ou na entrada da planta) para evitar sobretensa˜o no motor ou que o carro patine no trilho.

# 2.3 Sistema de controle com resposta deatbeat

Discretize a fun¸c˜ao de transferˆencia (1) e projete um controlador de modo que o sistema em malha fechada tenha resposta deadbeat para entrada degrau (e onda quadrada). Veriﬁque se a a¸c˜ao de controle ultrapassa o valor ma´ximo de tens˜ao que o motor pode suportar. Nesse caso, refa¸a o projeto aumentando o tempo necess´ario para que o erro passe a ser nulo e veriﬁque novamente se a a¸c˜ao de controle pode ser implementada. Ao implementar o controlador, limite a tens˜ao na sa´ıda do controlador (ou na entrada da planta) para evitar sobretens˜o no motor ou que o carro patine no trilho.

# 2.4 Controle PI no espa¸co de estados

Discretize a descri¸c˜ao de estados (2). Para implementar a a¸c˜ao integral aumente a planta como explicado na sec¸˜ao 6-7 do livro Ogata. Projete uma realimentac¸˜ao de estados para o sistema escolhendo autovalores que garantam um desempenho especiﬁcado para resposta transito´ria e estaciona´ria. Se necess´ario, projete um estimador de estados. Veriﬁque se a¸c˜ao de controle ultrapassa o limite do motor e, nesse caso, reveja as especiﬁca¸c˜oes do projeto. Implemente o controlador com limita¸c˜ao de tens˜ao na sa´ıda (ou na entrada da planta) para evitar sobretens˜o no motor ou que o carro patine no trilho.

# 3 Outras informa¸co˜es

Todas as aulas a partir de 28/05 ser˜ao no Laborat´orio de Controle (SG-11). A presen¸a nos dias e hora´rios de aula designados para seu grupo ´e obrigat´oria e contabilizada na frequˆencia. A chamada ser´a feita depois de 10 minutos do in´ıcio hora´rio designado e os alunos devera˜o permanecer durante todo o per´ıodo. Os grupos devem ter 2 alunos 1 . N˜ao est´a prevista a utiliza¸˜ao do laborat´orio fora do hora´rio de aula. Recomenda-se, portanto, uma boa programac¸˜ao para utiliza¸˜ao do tempo. O relat´rio deve ter resumo, introdu¸c˜ao, modelagem (e identiﬁcac¸˜ao de paraˆmetros),

projeto, resultados (de simula¸˜ao e experimentais), conclus˜oes e bibliograﬁa. Deve ter informa¸c˜oes suﬁcientes para que outro aluno da disciplina possa reproduzir o experimento e obter os mesmos resultados. Todas as escolhas, como de per´ıodo de amostragem ou especiﬁca¸c˜oes de projeto, devem ser justiﬁcadas. A data de entrega do relato´rio ´e 04/07. Os projetos devera˜o ser apresentados por todos os grupos nas aulas dos dias 04/07, 09/07 e 11/07. Na apresentac¸˜ao, todos os componentes do grupo ser˜ao questionados pelo professor e recebera˜o notas individualmente.

1 Sera˜o permitidos grupos de 3 alunos se todos os grupos j´ tiverem completos

