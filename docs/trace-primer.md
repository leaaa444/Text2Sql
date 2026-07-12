# Primer kompletnog traga (trace) kroz agentni graf

**Pitanje:** Koliko filmova je u kategoriji 'Comedy'?

## Koraci kroz cvorove

| # | Cvor (patern) | Ishod |
|---|---|---|
| 1 | `recorder_load` | 0 prethodnih pitanja |
| 2 | `retriever` | ucitana sema baze |
| 3 | `scope` | u temi |
| 4 | `selector` | samostalno pitanje, bez izmene |
| 5 | `planner` | 3 korak(a) |
| 6 | `deliberator` | generisan SQL (2 primera) |
| 7 | `integrator` | validan |
| 8 | `guard` | bezbedan, +LIMIT |
| 9 | `executor` | 1 redova |
| 10 | `presenter` | napisan sazetak |
| 11 | `recorder_save` | zapamceno pitanje |

## Plan (Planner)

1. Identificirati ID kategorije 'Comedy' iz tabele category.
2. Pronaći sve filmove koji pripadaju toj kategoriji koristeći tabelu film_category.
3. Prebrojati broj filmova koji su pronađeni u prethodnom koraku.

## Generisani SQL (Deliberator, posle Guard-a)

```sql
SELECT
  COUNT(*)
FROM film AS f
JOIN film_category AS fc
  ON f.film_id = fc.film_id
JOIN category AS c
  ON fc.category_id = c.category_id
WHERE
  c.name = 'Comedy'
LIMIT 100
```

## Rezultat

**Odgovor (Presenter):** U kategoriji 'Comedy' ima 143 filma.

**Broj LLM poziva:** 4 · **Vreme:** 11.2 s · **Samoispravljanja:** 0
