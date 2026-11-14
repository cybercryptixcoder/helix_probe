"""Register MIT's hand-written MinAtar Breakout policy as a target, with an input set of real game states.

The network is from the MIT Sparks logs (github.com/RikiyaT/lm_understand-logs, CC BY 4.0), experiment 5: GPT-6 Astra
wrote every weight of a 600-32-32-6 tanh policy for MinAtar Breakout in one reply, with no training. Its design is
therefore known (the reply describes it), it cannot have been memorised by a reader, and, unlike MIT's PPO game
policies in experiment 1, its environment is public (the MinAtar package), so real input states can be generated.

What this script does:
  1. loads the network (exp5_write_from_scratch/networks/breakout/hand.npz);
  2. plays MinAtar Breakout with it exactly as MIT scored it (actions sampled from the softmax, sticky actions 0.1),
     building the 600-number observation the way MIT's prompt defines it, and checks that the score is in the range
     MIT reports (mean 517 over 1,000 episodes): that confirms the observation is built correctly;
  3. saves 6,000 distinct visited states as the input set (inputs.npy), plus the weights and meta.json.

Needs:  pip install minatar==1.0.15   and the logs:  git clone https://github.com/RikiyaT/lm_understand-logs
Run:    SPARKS_LOGS=/path/to/lm_understand-logs python3 lab/targets/build_minatar.py
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(HERE, "..", "models")
SPARKS = os.environ.get("SPARKS_LOGS", "/home/claude/ext/lm_understand-logs")
TID = "astra_breakout"


def observe(env):
    """MIT's 600-number observation: index = (row * 10 + column) * 6 + channel; channels 0 player (paddle), 1 danger
    (empty), 2 reward (bricks), 3 projectile (ball), 4 trail, 5 gauge (empty)."""
    s = env.state()                                   # [10, 10, 4]: paddle, ball, trail, brick
    o = np.zeros((10, 10, 6), np.float64)
    o[:, :, 0], o[:, :, 2], o[:, :, 3], o[:, :, 4] = s[:, :, 0], s[:, :, 3], s[:, :, 1], s[:, :, 2]
    return o.reshape(600)


def main():
    from minatar.environments.breakout import Env
    raw = np.load(os.path.join(SPARKS, "exp5_write_from_scratch", "networks", "breakout", "hand.npz"))
    W = {"W1": raw["actor/dense1/kernel"], "b1": raw["actor/dense1/bias"], "W2": raw["actor/dense2/kernel"],
         "b2": raw["actor/dense2/bias"], "W3": raw["actor/logits/kernel"], "b3": raw["actor/logits/bias"]}
    W = {k: v.astype(np.float64) for k, v in W.items()}

    def logits(x):
        return np.tanh(np.tanh(x @ W["W1"] + W["b1"]) @ W["W2"] + W["b2"]) @ W["W3"] + W["b3"]

    rng = np.random.default_rng(0)
    seen, scores = {}, []
    for ep in range(12):
        env = Env(); env.random = np.random.RandomState(ep); env.reset()
        prev, score, t = 0, 0, 0
        while not env.terminal and t < 4000:
            x = observe(env)
            if rng.random() < 0.5:
                seen.setdefault(x.astype(np.uint8).tobytes(), x)
            z = logits(x); p = np.exp(z - z.max()); p /= p.sum()
            a = int(rng.choice(6, p=p))
            if rng.random() < 0.1:
                a = prev                               # sticky actions
            r, _ = env.act(a)
            prev, score, t = a, score + r, t + 1
        scores.append(score / max(t, 1))
    per_step = float(np.mean(scores))
    # MIT: 517.4 points over a mean of 7,417 steps = 0.070 points per step. A random policy loses the ball at once.
    assert per_step > 0.05, f"the policy scores {per_step:.3f} points per step; MIT's figure is 0.070: the observation is wrong"
    X = np.stack(list(seen.values()))
    X = X[rng.permutation(len(X))[:6000]].astype(np.int8)
    d = os.path.join(MODELS, TID)
    os.makedirs(d, exist_ok=True)
    np.savez(os.path.join(d, "weights.npz"), **W)
    np.save(os.path.join(d, "inputs.npy"), X)
    order = ["W1", "b1", "W2", "b2", "W3", "b3"]
    answer_detail = ("Design, from the model's own reply (MIT logs, exp5, runs/breakout/reply/answer.md): the first layer computes four "
                     "landing-position errors (where the ball will come down, minus the paddle's column) for the ball descending right, "
                     "descending left, ascending right and ascending left, and two direction indicators read from the trail; descending "
                     "predictions include wall reflections. The second layer gates the left and right decisions and chooses no-op when "
                     "the paddle is already in place. 815 of the 20,486 weights are non-zero. Scored by MIT at 517 points per episode "
                     "(PPO at 500M steps: 25).")
    meta = {
        "id": TID, "name": "Hand-written game policy", "family": "MIT Sparks, written from scratch (CC BY 4.0)", "forward": "mlp_tanh",
        "order": order,
        "arch": ("A multilayer perceptron with 600 inputs, two hidden layers of 32 units with tanh, and 6 outputs.\n"
                 "  h1 = tanh(x @ W1 + b1);  h2 = tanh(h1 @ W2 + b2);  out = h2 @ W3 + b3\n"
                 "The network's decision is its largest output."),
        "context": ("The input is a 10 x 10 grid with 6 binary channels; input index = (row * 10 + column) * 6 + channel, rows 0 (top) "
                    "to 9 (bottom). Channels: 0 player, 1 danger, 2 reward, 3 projectile, 4 trail, 5 gauge. The 6 outputs are logits for "
                    "the actions no-op, left, up, right, down, fire. The network is a policy for a MinAtar game."),
        "tensor_desc": {"W1": "layer 1 weights (row i = input i)", "W2": "layer 2 weights", "W3": "output weights (column = output)"},
        "answer": {"short": "a policy for MinAtar Breakout: move the paddle under where the ball will land", "detail": answer_detail},
        "source": ("MIT Sparks logs, exp5_write_from_scratch/networks/breakout/hand.npz (written by GPT-6 Astra in one reply; CC BY 4.0). "
                   "Input states generated here by playing MinAtar 1.0.15 Breakout with the network (lab/targets/build_minatar.py)."),
        "perm_groups": [{"size": 32, "members": [["W1", 1], ["b1", 0], ["W2", 0]]}, {"size": 32, "members": [["W2", 1], ["b2", 0], ["W3", 0]]}],
        "input": "600 numbers that are each 0 or 1, shape [B, 600]",
        "domain": {"file": "inputs.npy",
                   "text": f"The network is used on inputs of 600 numbers that are each 0 or 1. X holds {len(X):,} such inputs, a sample of the "
                           "inputs it meets in use."},
        "score_check": {"points_per_step": per_step, "mit_points_per_step": 517.411 / 7417.202, "states_collected": int(len(seen))},
    }
    meta["tensors"] = [{"name": k, "shape": list(W[k].shape), "desc": meta["tensor_desc"].get(k, "")} for k in order]
    meta["params"] = int(sum(W[k].size for k in order))
    json.dump(meta, open(os.path.join(d, "meta.json"), "w"), indent=1)
    acts = logits(X.astype(np.float64)).argmax(1)
    print(f"{TID}: {per_step:.3f} points per step (MIT: {517.411 / 7417.202:.3f}); {len(seen):,} distinct states seen, {len(X):,} kept; "
          f"decisions on them: {np.bincount(acts, minlength=6).tolist()} (no-op, left, up, right, down, fire)")


if __name__ == "__main__":
    main()
