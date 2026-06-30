# Raport z laboratorium LLMOps

## Cel zadania

Celem laboratorium było przygotowanie prostego projektu LLMOps, uruchomienie inferencji modelu oraz dodanie GitHub Actions.

## Próba uruchomienia vLLM

Podjęto próbę uruchomienia modelu Qwen/Qwen3-1.7B za pomocą vLLM.

Podczas uruchamiania pojawił się błąd:

`RuntimeError: Failed to infer device type`

Następnie sprawdzono komendę `nvidia-smi`. System zwrócił informację, że komenda nie została znaleziona, co oznacza brak dostępnego środowiska NVIDIA/CUDA dla vLLM.

## Alternatywna inferencja modelu

Ze względu na problem środowiskowy z vLLM wykonano alternatywną inferencję na CPU z użyciem biblioteki `transformers` oraz małego modelu testowego `sshleifer/tiny-gpt2`.

Model został poprawnie pobrany, uruchomiony na CPU, przyjął prompt i wygenerował odpowiedź tekstową.

Przykładowy prompt:

`LLMOps is important because`

Przykładowy wynik:

`LLMOps is important because stairs stairs stairs...`

Oznacza to, że inferencja modelu zakończyła się sukcesem technicznym, ponieważ model przyjął wejście i wygenerował tekst.

## GitHub Actions

Dodano workflow GitHub Actions w pliku:

`.github/workflows/actions.yml`

Workflow instaluje zależności i uruchamia testy automatyczne przy każdym wysłaniu kodu do repozytorium.

## Wniosek

Projekt zawiera kod laboratoryjny, raport oraz konfigurację GitHub Actions. Ze względu na brak dostępnej karty NVIDIA/CUDA vLLM nie został uruchomiony lokalnie, ale wykonano alternatywną inferencję modelu na CPU.
