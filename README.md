# ctfd_rate-by-openai

1. Configure plugin using config files by removing `.example` in `config` directory
 - **criteria.md** - Fill up rate criteria
 - **ctfd_api.conf** - CTFd API config (token & URL)
 - **openai_config.py** - OpenAI config

2. Run a script `script`

3. `docker-compose up` in CTFd directory

4. Run `api_script` from `config` directory
 - `./api_script` after API token config