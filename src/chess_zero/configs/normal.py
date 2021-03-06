class PlayDataConfig:
    def __init__(self):
        self.nb_game_in_file = 100
        self.sl_nb_game_in_file = 100
        self.max_file_num = 200  # 5000


class PlayConfig:
    def __init__(self):
        self.max_processes = 8
        self.search_threads = 16
        self.vram_frac = 1.0
        self.simulation_num_per_move = 800
        self.c_puct = 3
        self.noise_eps = 0.25
        self.dirichlet_alpha = 0.3
        self.change_tau_turn = 80
        self.automatic_draw_turn = 100
        self.virtual_loss = 3
        self.parallel_search_num = 16
        self.prediction_worker_sleep_sec = 0.0001
        self.wait_for_expanding_sleep_sec = 0.00001
        self.resign_threshold = None
        self.min_resign_turn = 10
        self.random_endgame = -1  # -1 for regular play, n > 2 for randomly generated endgames with n pieces.
        self.tablebase_access = False


class EvaluateConfig:
    def __init__(self):
        self.game_num = 100  # 400
        self.replace_rate = 0.55
        self.play_config = PlayConfig()
        self.play_config.simulation_num_per_move = 200
        self.play_config.noise_eps = 0
        self.random_endgame = -1
        self.play_config.tablebase_access = False


class PlayWithHumanConfig:
    def __init__(self):
        self.play_config = PlayConfig()
        self.play_config.tablebase_access = False


class TrainerConfig:
    def __init__(self):
        self.batch_size = 32  # 2048
        self.cleaning_processes = 8  # RAM explosion...
        self.vram_frac = 1.0
        self.epoch_to_checkpoint = 1
        self.start_total_steps = 0
        self.save_model_steps = 10000
        self.load_data_steps = 1000
        self.min_data_size_to_learn = 10000
        self.max_num_files_in_memory = 20


class ModelConfig:
    def __init__(self):
        self.cnn_filter_num = 256
        self.cnn_filter_size = 3
        self.res_layer_num = 19  # was 7, why? should this be 19 or 39?
        self.l2_reg = 1e-4
        self.value_fc_size = 256
        self.t_history = 8
        self.input_stack_height = 7 + self.t_history*14
