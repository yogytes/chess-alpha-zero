import os
from logging import getLogger
from random import random
from time import sleep
import chess
from chess_zero.agent.model_chess import ChessModel
from chess_zero.agent.player_chess import ChessPlayer
from chess_zero.config import Config
from chess_zero.env.chess_env import ChessEnv, Winner
from chess_zero.lib import tf_util
from chess_zero.lib.data_helper import get_next_generation_model_dirs
from chess_zero.lib.model_helper import save_as_best_model, load_best_model_weight

logger = getLogger(__name__)


def start(config: Config):
    tf_util.set_session_config(per_process_gpu_memory_fraction=0.2)
    return EvaluateWorker(config).start()


class EvaluateWorker:
    def __init__(self, config: Config):
        """

        :param config:
        """
        self.config = config
        self.best_model = None

    def start(self):
        self.best_model = self.load_best_model()

        while True:
            ng_model, model_dir = self.load_next_generation_model()
            logger.debug(f"start evaluate model {model_dir}")
            ng_is_great = self.evaluate_model(ng_model)
            if ng_is_great:
                logger.debug(f"new model becomes the best model: {model_dir}")
                save_as_best_model(ng_model)
                self.best_model = ng_model
            self.remove_model(model_dir)

    def evaluate_model(self, ng_model):
        results = []
        winning_rate = 0
        for game_idx in range(self.config.eval.game_num):
            # ng_win := if ng_model win -> 1, lose -> 0, draw -> None
            ng_win, ng_is_white = self.play_game(self.best_model, ng_model)
            if ng_win is not None:
                results.append(ng_win)
                winning_rate = sum(results) / len(results)
            logger.debug(f"game {game_idx}: ng won = {ng_win}, ng played white = {ng_is_white}, winning rate = {winning_rate*100:.1f}%")
            if results.count(0) >= self.config.eval.game_num * (1-self.config.eval.replace_rate):
                logger.debug(f"lose count has reached {results.count(0)}, so give up challenge")
                break
            if results.count(1) >= self.config.eval.game_num * self.config.eval.replace_rate:
                logger.debug(f"win count has reached {results.count(1)}, so change best model")
                break

        winning_rate = sum(results) / len(results) if len(results) != 0 else 0
        logger.debug(f"winning rate {winning_rate*100:.1f}%")
        return winning_rate >= self.config.eval.replace_rate

    def play_game(self, best_model, ng_model):
        env = ChessEnv().reset()

        ng_player = ChessPlayer(self.config, ng_model, play_config=self.config.eval.play_config)
        best_player = ChessPlayer(self.config, best_model, play_config=self.config.eval.play_config)
        ng_is_white = random() < 0.5

        while not env.done:
            ai = ng_player if ng_is_white == (env.board.turn == chess.WHITE) else best_player
            action = ai.action(env.observation)
            env.step(action)

        ng_win = None
        if env.winner != Winner.DRAW:
            ng_win = ng_is_white == (env.winner == Winner.WHITE)
        return ng_win, ng_is_white

    def load_best_model(self):
        model = ChessModel(self.config)
        load_best_model_weight(model)
        return model

    def load_next_generation_model(self):
        rc = self.config.resource
        while True:
            dirs = get_next_generation_model_dirs(self.config.resource)
            if dirs:
                break
            logger.info(f"there is no next-generation model to evaluate")
            sleep(60)
        model_dir = dirs[-1] if self.config.eval.evaluate_latest_first else dirs[0]
        config_path = os.path.join(model_dir, rc.next_generation_model_config_filename)
        weight_path = os.path.join(model_dir, rc.next_generation_model_weight_filename)
        model = ChessModel(self.config)
        model.load(config_path, weight_path)
        return model, model_dir

    def remove_model(self, model_dir):
        rc = self.config.resource
        config_path = os.path.join(model_dir, rc.next_generation_model_config_filename)
        weight_path = os.path.join(model_dir, rc.next_generation_model_weight_filename)
        os.remove(config_path)
        os.remove(weight_path)
        os.rmdir(model_dir)
