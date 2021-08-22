import torch.nn.functional as F


def train_model(model, optimizer, dataset_training, dataset_validation=None, n_epoch=10):
    """Trains model."""
    idx = 0
    best_val_loss = 10000
    for i in range(n_epoch):
        model.train()
        total = 0
        sum_loss = 0
        for x, y_bb in dataset_training:
            batch = x.shape[0]
            x = x.cuda().float()
            y_bb = y_bb.cuda().float()
            out_bb = model(x)
            if i == n_epoch-1:
                print(out_bb, y_bb)
            loss = F.l1_loss(out_bb, y_bb, reduction="none").sum(1).sum()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            idx += 1
            total += batch
            sum_loss += loss.item()
        train_loss = sum_loss/total
        if dataset_validation is not None:
            val_loss = run_validation(model, dataset_validation)
            print("train_loss %.3f val_loss %.3f val_acc %.3f" % (train_loss, val_loss, val_acc))
            if val_loss < best_val_loss:
                best_model = model
                best_val_loss = val_loss
        else:
            print("train_loss %.3f" % (train_loss))
            best_model = model
    return best_model


def run_validation(model, dataset_validation):
    """Runs model on the validation dataset and compute validation metrics."""
    model.eval()
    total = 0
    sum_loss = 0
    for x, y_bb in dataset_validation:
        batch = y_bb.shape[0]
        x = x.cuda().float()
        y_bb = y_bb.cuda().float()
        out_bb = model(x)
        loss = F.l1_loss(out_bb, y_bb, reduction="none").sum(1).sum()
        sum_loss += loss.item()
        total += batch
    return sum_loss/total


def update_optimizer(optimizer, lr):
    """Changes learning rate."""
    for i, param_group in enumerate(optimizer.param_groups):
        param_group["lr"] = lr
