class EvaluateConfig:
    def __init__(self):
        self.game_num = 10  # 10
        self.replace_rate = 0.55
        self.play_config = PlayConfig()
        self.play_config.simulation_num_per_move = 50
        self.play_config.thinking_loop = 1
        self.play_config.c_puct = 1
        self.play_config.change_tau_turn = 0
        self.play_config.noise_eps = 0
        self.evaluate_latest_first = True


class PlayDataConfig:
    def __init__(self):
        self.nb_game_in_file = 20  # 100
        self.max_file_num = 50  # 10


class PlayConfig:
    def __init__(self):
        self.simulation_num_per_move = 50  # 10
        self.thinking_loop = 1
        self.logging_thinking = False
        self.c_puct = 3  # 5
        self.noise_eps = 0.25
        self.dirichlet_alpha = 0.03
        self.change_tau_turn = 10
        self.virtual_loss = 3
        self.prediction_queue_size = 16
        self.parallel_search_num = 16 # 4
        self.prediction_worker_sleep_sec = 0.00001
        self.wait_for_expanding_sleep_sec = 0.000001
        self.resign_threshold = None  #-1.0
        self.min_resign_turn = 10


class TrainerConfig:
    def __init__(self):
        self.batch_size = 512  # 2048
        self.epoch_to_checkpoint = 1
        self.start_total_steps = 0
        self.save_model_steps = 2000
        self.load_data_steps = 1000


class ModelConfig:
    cnn_filter_num = 128
    cnn_filter_size = 3
    res_layer_num = 7
    l2_reg = 1e-4
    value_fc_size = 128