import sys
import os
from pathlib import Path

# Ajouter le répertoire racine du projet au chemin Python
sys.path.append(str(Path(__file__).parent.resolve()))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )