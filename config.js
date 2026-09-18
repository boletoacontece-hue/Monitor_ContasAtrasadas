// Configuração do painel — preencha com os dados do seu projeto Supabase.
// A chave "anon" é pública por natureza (a segurança vem das políticas RLS).
// NUNCA coloque aqui a chave "service_role".
window.ACONTECE_CONFIG = {
  SUPABASE_URL: "https://rozlxguovdbcchqghcbm.supabase.co",
  SUPABASE_ANON_KEY: "sb_publishable_bmhz3OoA2Xn_Z7-Mn228nQ_QR4HYU8u",

  // Fonte dos dados: "supabase" (produção, protegido por login+RLS)
  // ou "json" (apenas dev local, lê data/dados.json — NÃO publique com este modo).
  DATA_SOURCE: "supabase",

  // Nomes das tabelas (conforme supabase/schema.sql)
  TABLE_LANC: "ctapag_lancamentos",
  TABLE_CONF: "ctapag_conferencia",
  TABLE_TRAT: "ctapag_tratativas"
};
