def test_cv():
    try:
        import ray
    except ImportError:
        return
    from flaml import AutoML

    from datasets import load_dataset

    train_dataset = (
        load_dataset("glue", "mrpc", split="train[:1%]").to_pandas().iloc[0:4]
    )

    custom_sent_keys = ["sentence1", "sentence2"]
    label_key = "label"

    X_train = train_dataset[custom_sent_keys]
    y_train = train_dataset[label_key]

    automl = AutoML()

    automl_settings = {
        "gpu_per_trial": 0,
        "max_iter": 3,
        "time_budget": 20,
        "task": "seq-classification",
        "metric": "accuracy",
        "n_splits": 3,
        "model_history": True,
    }

    automl_settings["custom_hpo_args"] = {
        "model_path": "google/electra-small-discriminator",
        "output_dir": "data/output/",
        "ckpt_per_epoch": 1,
        "fp16": False,
    }

    automl.fit(X_train=X_train, y_train=y_train, **automl_settings)
