PRAGMA foreign_keys = OFF;

-- ==================== LIMPEZA ====================
DELETE FROM evento_fogo_despacho;
DELETE FROM evento_fogo_relatorioocorrencia;
DELETE FROM evento_fogo_ordemservico;
DELETE FROM gestao_noticiafogo;
DELETE FROM evento_fogo_eventofogo;
DELETE FROM gestao_equipe;
DELETE FROM usuario_bombeiro;
DELETE FROM usuario_usuario;
DELETE FROM usuario_escala;
DELETE FROM gestao_guarnicao;

-- ==================== GUARNIÇÕES ====================
INSERT INTO gestao_guarnicao (id, codigo, nome, cep) VALUES
  (1, 101, 'CBM - Cuiabá',                 '78005000'),
  (2, 102, 'CBM - Várzea Grande',          '78110000'),
  (3, 103, 'CBM - Rondonópolis',           '78700000'),
  (4, 104, 'CBM - Sinop',                  '78550000'),
  (5, 105, 'CBM - Chapada dos Guimarães',  '78195000');

-- ==================== ESCALAS ====================
INSERT INTO usuario_escala (id, codigo, id_guarnicao_id, data_inicio, data_fim, estatus) VALUES
  (1, 2001, 1, date('now', '+3 days'),  date('now', '+9 days'),  'LIVRE'),
  (2, 2002, 2, date('now', '+10 days'), date('now', '+16 days'), 'LIVRE'),
  (3, 2003, 3, date('now', '+17 days'), date('now', '+23 days'), 'LIVRE'),
  (4, 2004, 4, date('now', '+24 days'), date('now', '+30 days'), 'LIVRE'),
  (5, 2005, 5, date('now', '+31 days'), date('now', '+37 days'), 'LIVRE');

-- ==================== USUÁRIOS (1 a 3 = comando) ====================
INSERT INTO usuario_usuario (id, nome, email, perfil) VALUES
  (1,  'Juan Pablo Ferreira',      'juan.ferreira@cbm.mt.gov.br',     'COMANDO'),
  (2,  'Mariana Alves Duarte',     'mariana.duarte@cbm.mt.gov.br',    'COMANDO'),
  (3,  'Rodrigo Menezes Barros',   'rodrigo.barros@cbm.mt.gov.br',    'COMANDO'),
  (4,  'Camila Souza Ribeiro',     'camila.ribeiro@cbm.mt.gov.br',    'COMBATENTE'),
  (5,  'Thiago Nascimento Lima',   'thiago.lima@cbm.mt.gov.br',       'COMBATENTE'),
  (6,  'Larissa Martins Costa',    'larissa.costa@cbm.mt.gov.br',     'COMBATENTE'),
  (7,  'Gabriel Oliveira Santos',  'gabriel.santos@cbm.mt.gov.br',    'COMBATENTE'),
  (8,  'Beatriz Carvalho Rocha',   'beatriz.rocha@cbm.mt.gov.br',     'COMBATENTE'),
  (9,  'Felipe Araújo Teixeira',   'felipe.teixeira@cbm.mt.gov.br',   'COMBATENTE'),
  (10, 'Isabela Pereira Gomes',    'isabela.gomes@cbm.mt.gov.br',     'COMBATENTE'),
  (11, 'Lucas Henrique Moraes',    'lucas.moraes@cbm.mt.gov.br',      'COMBATENTE'),
  (12, 'Amanda Cristina Pinto',    'amanda.pinto@cbm.mt.gov.br',      'COMBATENTE'),
  (13, 'Matheus Correia Dias',     'matheus.dias@cbm.mt.gov.br',      'COMBATENTE'),
  (14, 'Fernanda Lopes Cardoso',   'fernanda.cardoso@cbm.mt.gov.br',  'COMBATENTE'),
  (15, 'Eduardo Batista Freitas',  'eduardo.freitas@cbm.mt.gov.br',   'COMBATENTE');

-- ==================== BOMBEIROS ====================
-- matrículas 1001 a 1015; os 8 primeiros em escala (INDISPONIVEL), os demais LIVRE.
-- a equipe é ligada depois, por causa da dependência circular Equipe <-> Bombeiro.
INSERT INTO usuario_bombeiro (matricula, id_usuario_id, id_equipe_id, id_escala_id, estatus, proficiencia) VALUES
  (1001, 1,  NULL, 1,    'INDISPONIVEL', NULL),
  (1002, 2,  NULL, 2,    'INDISPONIVEL', NULL),
  (1003, 3,  NULL, 3,    'INDISPONIVEL', NULL),
  (1004, 4,  NULL, 4,    'INDISPONIVEL', NULL),
  (1005, 5,  NULL, 5,    'INDISPONIVEL', NULL),
  (1006, 6,  NULL, 1,    'INDISPONIVEL', NULL),
  (1007, 7,  NULL, 2,    'INDISPONIVEL', NULL),
  (1008, 8,  NULL, 3,    'INDISPONIVEL', NULL),
  (1009, 9,  NULL, NULL, 'LIVRE',        NULL),
  (1010, 10, NULL, NULL, 'LIVRE',        NULL),
  (1011, 11, NULL, NULL, 'LIVRE',        NULL),
  (1012, 12, NULL, NULL, 'LIVRE',        NULL),
  (1013, 13, NULL, NULL, 'LIVRE',        NULL),
  (1014, 14, NULL, NULL, 'LIVRE',        NULL),
  (1015, 15, NULL, NULL, 'LIVRE',        NULL);

-- ==================== EQUIPES (comandantes: 1001, 1002, 1003) ====================
INSERT INTO gestao_equipe (id, codigo, estatus, id_comandante_id) VALUES
  (1, 301, 'LIVRE', 1001),
  (2, 302, 'LIVRE', 1002),
  (3, 303, 'LIVRE', 1003);

UPDATE usuario_bombeiro SET id_equipe_id = ((matricula - 1001) % 3) + 1;

-- ==================== EVENTOS DE FOGO ====================
-- latitude/longitude são IntegerField no model, então ficam em graus inteiros.
INSERT INTO evento_fogo_eventofogo (id, codigo, data_registro, longitude, latitude, estatus, descricao) VALUES
  (1,  20260001, datetime('now', '-1 days'),  -56, -15, 'ABERTO',    'Queimada em pastagem na região de Cuiabá'),
  (2,  20260002, datetime('now', '-2 days'),  -56, -16, 'COMBATE',   'Incêndio em vegetação no Parque Nacional da Chapada dos Guimarães'),
  (3,  20260003, datetime('now', '-3 days'),  -55, -16, 'COMBATE',   'Fogo em área de cerrado próxima à BR-163, Rondonópolis'),
  (4,  20260004, datetime('now', '-4 days'),  -55, -12, 'ABERTO',    'Foco de calor em lavoura de soja, Sinop'),
  (5,  20260005, datetime('now', '-6 days'),  -56, -15, 'ENCERRADO', 'Incêndio em terreno baldio em Várzea Grande'),
  (6,  20260006, datetime('now', '-8 days'),  -57, -16, 'ENCERRADO', 'Queimada às margens do Rio Cuiabá controlada pela equipe'),
  (7,  20260007, datetime('now', '-10 days'), -55, -15, 'COMBATE',   'Fogo em reserva legal no entorno de Poconé'),
  (8,  20260008, datetime('now', '-12 days'), -56, -14, 'ABERTO',    'Foco de incêndio em mata ciliar, Nobres'),
  (9,  20260009, datetime('now', '-15 days'), -54, -15, 'ENCERRADO', 'Queimada em fazenda de gado, Primavera do Leste'),
  (10, 20260010, datetime('now', '-20 days'), -58, -17, 'ENCERRADO', 'Incêndio no Pantanal, região de Cáceres');

-- ==================== ORDENS DE SERVIÇO ====================
-- uma por evento (OneToOne): eventos 1, 2, 3, 5 e 6
INSERT INTO evento_fogo_ordemservico (id, id_evento_fogo_id, data_emissao, estatus) VALUES
  (1, 1, datetime('now', '-1 days', '+1 hours'),  'ABERTA'),
  (2, 2, datetime('now', '-2 days', '+1 hours'),  'ANDAMENTO'),
  (3, 3, datetime('now', '-3 days', '+2 hours'),  'ANDAMENTO'),
  (4, 5, datetime('now', '-6 days', '+1 hours'),  'FECHADA'),
  (5, 6, datetime('now', '-8 days', '+2 hours'),  'FECHADA');

-- ==================== RELATÓRIOS DE OCORRÊNCIA ====================
INSERT INTO evento_fogo_relatorioocorrencia (id, codigo, id_os_id, data, descricao) VALUES
  (1, 7001, 2, datetime('now', '-2 days', '+4 hours'),  'Equipe chegou ao local e iniciou o combate com abafadores e caminhão-pipa.'),
  (2, 7002, 2, datetime('now', '-1 days', '+2 hours'),  'Foco principal contido; permanece monitoramento de reignição na borda do parque.'),
  (3, 7003, 3, datetime('now', '-3 days', '+5 hours'),  'Fogo se propagou ao longo da rodovia; trânsito parcialmente interditado.'),
  (4, 7004, 4, datetime('now', '-6 days', '+6 hours'),  'Incêndio extinto sem vítimas e sem danos a edificações vizinhas.');

-- ==================== NOTÍCIAS ====================
INSERT INTO gestao_noticiafogo (id, id_evento_fogo_id, titulo, descricao, data) VALUES
  (1, 2, 'Incêndio atinge vegetação na Chapada dos Guimarães',
      'Equipes do Corpo de Bombeiros combatem um incêndio em área de vegetação nativa na Chapada dos Guimarães. Brigadistas e viaturas foram mobilizados e o acesso a trilhas da região está restrito por segurança.',
      date('now', '-2 days')),
  (2, 3, 'Fogo próximo à BR-163 mobiliza bombeiros em Rondonópolis',
      'Um incêndio em área de cerrado às margens da BR-163 exigiu o trabalho de duas guarnições. A fumaça reduziu a visibilidade na rodovia e motoristas foram orientados a redobrar a atenção.',
      date('now', '-3 days')),
  (3, 5, 'Incêndio em terreno baldio é controlado em Várzea Grande',
      'O Corpo de Bombeiros controlou o fogo em um terreno baldio sem registro de feridos. A corporação reforça o alerta sobre os riscos de queimadas em período de estiagem.',
      date('now', '-6 days')),
  (4, 10, 'Bombeiros encerram combate a incêndio no Pantanal',
      'Após dias de trabalho em região de difícil acesso, as equipes concluíram o combate ao incêndio no Pantanal, em Cáceres. A área segue em observação para evitar novos focos.',
      date('now', '-20 days'));

PRAGMA foreign_keys = ON;