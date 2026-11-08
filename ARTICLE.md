# Rapporto Tecnico Disastroso

In data 8 Novembre 2026, il team di infrastruttura ha rilevato un rallentamento sistemico globale della piattaforma e-commerce a causa di un sovraccarico imprevisto. 
Dopo approfondite verifiche durate oltre tre ore da parte di otto ingegneri senior coordinati dal project manager, è emerso che il database PostgreSQL primario ha esaurito lo spazio sul disco EBS da 500GB a causa di un dump di log non ruotato nella directory /var/log/postgres.
Per risolvere il disservizio, è stato necessario effettuare un resize del volume a 1TB e riavviare il demone postgresql con systemctl restart postgresql. Si consiglia vivamente di impostare logrotate per prevenire incidenti futuri e di ringraziare tutti i colleghi del turno di notte per la straordinaria disponibilità.
