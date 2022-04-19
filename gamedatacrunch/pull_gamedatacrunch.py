from download import download_base
from technames_meta import technames_metadata_table
from apps_techname_list import retrieve_engines_sdks_by_app_id

# Run this script to download all GameDataCrunch steam games and their sdk and engine types

download_base()
technames_metadata_table()
retrieve_engines_sdks_by_app_id()