import os
import re
import json

from openai import OpenAI

import settings


class OpenAiClient:
    def __init__(self):
        self.client =  OpenAI(api_key=settings.OPEN_API_KEY)

    def generate_strategy(self, account_id, campaign_metrics, keyword_metrics):
        print("ChatGPT is reading campaigns and keywords...\n")
        strategies = []

        for campaign in campaign_metrics:
            campaign_name = re.sub(r'[^a-zA-Z/]', '', campaign['name']).replace('/', '_').lower()

            prompt = f"""    
                J'ai besoin que tu me sortes les KPI principaux de la campagne :
                {json.dumps(campaign, indent=2)}

                J'ai besoin d'une analyse et d'insights sur les mots-clés suivants :
                {json.dumps(keyword_metrics, indent=2)}

                Et avec tout ceci, fais-moi un bilan avec des recommandations synthétiques au format Markdown dont la structure est la suivante : 
                # Nom de la Campagne

                ## Analyse des Performances

                - Point clé 1
                - Point clé 2
                - Point clé 3

                ## Recommandations

                1. Recommandation 1
                2. Recommandation 2
                3. Recommandation 3

                ## Nouveaux Mots-clés Suggérés

                - Nouveau mot-clé 1
                - Nouveau mot-clé 2
                - Nouveau mot-clé 3
            """

            response = self.client.chat.completions.create(
                model="chatgpt-4o-latest",
                messages=[{ "role": "user", "content": prompt}]
            )

            strategy_markdown = response.choices[0].message.content
            folder_path = f"strategies/{account_id}"
            os.makedirs(folder_path, exist_ok=True)

            file_name = os.path.join(
                folder_path,
                f"{campaign_name}_strategy.md"
            )
            with open(file_name, "w", encoding="utf-8'") as f:
                f.write(strategy_markdown)
                print(f"La stratégie a été générée et sauvegardée dans {file_name}\n")

            strategies.append(file_name)

        print(f"{len(strategies)} campaigns strategies generated")
