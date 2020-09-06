noob(neo).
disenchanted(trinity).
loves(trinity, neo).
visitsoracle(X) :- noob(X).
visitsoracle(X) :- disenchanted(X).
pickstheone(X) :- visitsoracle(X).
oraclesaysnottheone(X) :- noob(X), visitsoracle(X).
disenchanted :- noob(X), visitsoracle(X).
theone(X) :- oraclesaysnottheone(X), loves(Y, X), pickstheone(Y).

count(E, [], 0).
count(E, [E|T], N) :-  count(E,T,M), N is M+1.
count(E, [H|T], N) :- \+ E==H, count(E,T,N).

exactly1(L, E) :- count(L, E, 1).
atmost1(L, E) :- count(L, E, 1); count(L, E, 0).
atleast1(L, E) :- \+ count(L, E, 0).
