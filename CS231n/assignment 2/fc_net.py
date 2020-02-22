from builtins import range
from builtins import object
import numpy as np

from layers import *
from layer_utils import *


class TwoLayerNet(object):
    """
    A two-layer fully-connected neural network with ReLU nonlinearity and
    softmax loss that uses a modular layer design. We assume an input dimension
    of D, a hidden dimension of H, and perform classification over C classes.

    The architecure should be affine - relu - affine - softmax.

    Note that this class does not implement gradient descent; instead, it
    will interact with a separate Solver object that is responsible for running
    optimization.

    The learnable parameters of the model are stored in the dictionary
    self.params that maps parameter names to numpy arrays.
    """
    def __init__(self, input_dim=3*32*32, hidden_dim=100, num_classes=10,
                 weight_scale=1e-3, reg=0.0):
        """
        Initialize a new network.

        Inputs:
        - input_dim: An integer giving the size of the input
        - hidden_dim: An integer giving the size of the hidden layer
        - num_classes: An integer giving the number of classes to classify
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - reg: Scalar giving L2 regularization strength.
        """
        self.params = {
            'W1':np.random.randn(input_dim, hidden_dim) * weight_scale,
            'b1':np.zeros(hidden_dim),
            'W2':np.random.randn(hidden_dim, num_classes) * weight_scale,
            'b2':np.zeros(num_classes),
        }
        self.reg = reg  # 正则化因子

        ############################################################################
        # TODO: Initialize the weights and biases of the two-layer net. Weights    #
        # should be initialized from a Gaussian centered at 0.0 with               #
        # standard deviation equal to weight_scale, and biases should be           #
        # initialized to zero. All weights and biases should be stored in the      #
        # dictionary self.params, with first layer weights                         #
        # and biases using the keys 'W1' and 'b1' and second layer                 #
        # weights and biases using the keys 'W2' and 'b2'.                         #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################
        
    def loss(self, X, y=None):
            """
            Compute loss and gradient for a minibatch of data.

            Inputs:
            - X: Array of input data of shape (N, d_1, ..., d_k)
            - y: Array of labels, of shape (N,). y[i] gives the label for X[i].

            Returns:
            If y is None, then run a test-time forward pass of the model and return:
            - scores: Array of shape (N, C) giving classification scores, where
              scores[i, c] is the classification score for X[i] and class c.

            If y is not None, then run a training-time forward and backward pass and
            return a tuple of:
            - loss: Scalar value giving the loss
            - grads: Dictionary with the same keys as self.params, mapping parameter
              names to gradients of the loss with respect to those parameters.
            """
            scores = None
            ############################################################################
            # TODO: Implement the forward pass for the two-layer net, computing the    #
            # class scores for X and storing them in the scores variable.              #
            ############################################################################
            # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            # the architecture: affine-relu-affine-softmax
            # forward:
            out1, cache1 = affine_forward(X, self.params['W1'], self.params['b1']) 
            out2, cache2 = relu_forward(out1)
            out3, cache3 = affine_forward(out1, self.params['W2'], self.params['b2'])
            loss, dout1 = softmax_loss(out3, y)
            scores = out3
            
            # Compute gradient:
            dout2, dw2, db2 = affine_backward(dout1, cache3)
            dout3 = relu_backward(dout2, cache2)
            dx, dw, db = affine_backward(dout3, cache1)
            pass

            # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            ############################################################################
            #                             END OF YOUR CODE                             #
            ############################################################################

            # If y is None then we are in test mode so just return scores
            if y is None:
                return scores
            loss = loss + 0.5 * self.reg *(np.sum(self.params['W2']*self.params['W2']) 
              + np.sum(self.params['W1']*self.params['W1']))
            
            grads = {
                'W1':dw + self.reg * self.params['W1'],
                'b1':db,
                'W2':dw2 + self.reg * self.params['W2'],
                'b2':db2,
            }
            
            ############################################################################
            # TODO: Implement the backward pass for the two-layer net. Store the loss  #
            # in the loss variable and gradients in the grads dictionary. Compute data #
            # loss using softmax, and make sure that grads[k] holds the gradients for  #
            # self.params[k]. Don't forget to add L2 regularization!                   #
            #                                                                          #
            # NOTE: To ensure that your implementation matches ours and you pass the   #
            # automated tests, make sure that your L2 regularization includes a factor #
            # of 0.5 to simplify the expression for the gradient.                      #
            ############################################################################
            # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            

            # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
            ############################################################################
            #                             END OF YOUR CODE                             #
            ############################################################################

            return loss, grads


class FullyConnectedNet(object):
    """
    A fully-connected neural network with an arbitrary number of hidden layers,
    ReLU nonlinearities, and a softmax loss function. This will also implement
    dropout and batch/layer normalization as options. For a network with L layers,
    the architecture will be

    {affine - [batch/layer norm] - relu - [dropout]} x (L - 1) - affine - softmax

    where batch/layer normalization and dropout are optional, and the {...} block is
    repeated L - 1 times.

    Similar to the TwoLayerNet above, learnable parameters are stored in the
    self.params dictionary and will be learned using the Solver class.
    """

    def __init__(self, hidden_dims, input_dim=3*32*32, num_classes=10,
                 dropout=1, normalization=None, reg=0.0,
                 weight_scale=1e-2, dtype=np.float32, seed=None):
        """
        Initialize a new FullyConnectedNet.

        Inputs:
        - hidden_dims: A list of integers giving the size of each hidden layer.
        - input_dim: An integer giving the size of the input.
        - num_classes: An integer giving the number of classes to classify.
        - dropout: Scalar between 0 and 1 giving dropout strength. If dropout=1 then
          the network should not use dropout at all.
        - normalization: What type of normalization the network should use. Valid values
          are "batchnorm", "layernorm", or None for no normalization (the default).
        - reg: Scalar giving L2 regularization strength.
        - weight_scale: Scalar giving the standard deviation for random
          initialization of the weights.
        - dtype: A numpy datatype object; all computations will be performed using
          this datatype. float32 is faster but less accurate, so you should use
          float64 for numeric gradient checking.
        - seed: If not None, then pass this random seed to the dropout layers. This
          will make the dropout layers deteriminstic so we can gradient check the
          model.
        """
        self.normalization = normalization  # 正则化类型选择
        self.use_dropout = dropout != 1   # 是否使用 dropout
        self.reg = reg # 正则化强度
        self.num_layers = 1 + len(hidden_dims) # 网络层数 + 1 是最后的输出层
        self.dtype = dtype # 数据类型, float32 速度快精度低，用 float64 做 gradient check
        self.params = {} # 数据参数

        ############################################################################
        # TODO: Initialize the parameters of the network, storing all values in    #
        # the self.params dictionary. Store weights and biases for the first layer #
        # in W1 and b1; for the second layer use W2 and b2, etc. Weights should be #
        # initialized from a normal distribution centered at 0 with standard       #
        # deviation equal to weight_scale. Biases should be initialized to zero.   #
        #                                                                          #
        # When using batch normalization, store scale and shift parameters for the #
        # first layer in gamma1 and beta1; for the second layer use gamma2 and     #
        # beta2, etc. Scale parameters should be initialized to ones and shift     #
        # parameters should be initialized to zeros.                               #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        # 权重参数坐标从 1 开始计算。
        
        for num in range(self.num_layers):
            if num == 0:                            # 第一层的权重
                rows = input_dim                    # (D, H)
                cols = hidden_dims[num]             
            elif num == (self.num_layers -1):  # 最后一层的权重
                rows = hidden_dims[num-1]           # (H, C)
                cols = num_classes                  
            else:                                   # 中间的权重
                rows = hidden_dims[num-1]
                cols = hidden_dims[num]             # (H1, H2)

            self.params['W' + str(num+1)] = weight_scale * np.random.randn(rows, cols)   # (H1, H2)
            self.params['b' + str(num+1)] = np.zeros(cols)                               # (H2)  

            # 初始化bn层
            if (self.normalization == 'batchnorm') and (num != self.num_layers-1):     # 最后一层无BN
                self.params['gamma%d'%(num+1)] = np.ones(hidden_dims[num])             # 与隐层单元数一致 
                self.params['beta%d'%(num+1)] = np.zeros(hidden_dims[num]) 
            if (self.normalization == 'layernorm') and (num != self.num_layers-1):     # 最后一层无LN
                self.params['gamma%d'%(num+1)] = np.ones(hidden_dims[num])             # 与隐层单元数一致 
                self.params['beta%d'%(num+1)] = np.zeros(hidden_dims[num])      
        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # When using dropout we need to pass a dropout_param dictionary to each
        # dropout layer so that the layer knows the dropout probability and the mode
        # (train / test). You can pass the same dropout_param to each dropout layer.
        # dropout 参数 和 模式选择。
        self.dropout_param = {}
        if self.use_dropout:
            self.dropout_param = {'mode': 'train', 'p': dropout}
            if seed is not None:
                # seed 是随机种子
                self.dropout_param['seed'] = seed

        # With batch normalization we need to keep track of running means and
        # variances, so we need to pass a special bn_param object to each batch
        # normalization layer. You should pass self.bn_params[0] to the forward pass
        # of the first batch normalization layer, self.bn_params[1] to the forward
        # pass of the second batch normalization layer, etc.
        self.bn_params = []
        if self.normalization=='batchnorm':
            self.bn_params = [{'mode': 'train'} for i in range(self.num_layers - 1)]
        if self.normalization=='layernorm':
            self.bn_params = [{} for i in range(self.num_layers - 1)]

        # Cast all parameters to the correct datatype
        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Compute loss and gradient for the fully-connected net.

        Input / output: Same as TwoLayerNet above.
        """
        X = X.astype(self.dtype)
        mode = 'test' if y is None else 'train'

        # Set train/test mode for batchnorm params and dropout param since they
        # behave differently during training and testing.
        if self.use_dropout:
            self.dropout_param['mode'] = mode
        if self.normalization=='batchnorm':
            for bn_param in self.bn_params:
                bn_param['mode'] = mode
        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the fully-connected net, computing  #
        # the class scores for X and storing them in the scores variable.          #
        #                                                                          #
        # When using dropout, you'll need to pass self.dropout_param to each       #
        # dropout forward pass.                                                    #
        #                                                                          #
        # When using batch normalization, you'll need to pass self.bn_params[0] to #
        # the forward pass for the first batch normalization layer, pass           #
        # self.bn_params[1] to the forward pass for the second batch normalization #
        # layer, etc.                                                              #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        
        # 完成前向网络的计算, 略复杂，仔细看。
        cache = {}   # 来保存前向传播的值，用于之后的反向传播
        L = self.num_layers
        layer_input = X
        for num in range(L-1):                                     # L-1层  
            W = self.params['W%d'% (num+1)]                        # 使用权重的名称来访问参数
            b = self.params['b%d'% (num+1)]
            # h_out = 'h%d_out'% (num+1)                           # 为输出定义动态变量名称
            h_cache = 'h%d_cache'% (num+1)
            # relu_out = 'relu%d_out'% (num+1)
            relu_cache = 'relu%d_cache'% (num+1)

            h_out, cache[h_cache] = affine_forward(layer_input, W, b)      # 全连接层前向传播
            # BN层前向传播
            if self.normalization=='batchnorm':
                bn_cache = 'bn%d_cache'%(num+1)
                bn_out, cache[bn_cache] = batchnorm_forward(h_out, self.params['gamma%d'%(num+1)], 
                                                            self.params['beta%d'%(num+1)], self.bn_params[num])
                h_out = bn_out
            if self.normalization=='layernorm':
                ln_cache = 'ln%d_cache'%(num+1)
                ln_out, cache[ln_cache] = layernorm_forward(h_out, self.params['gamma%d'%(num+1)], 
                                                            self.params['beta%d'%(num+1)], self.bn_params[num])
                h_out = ln_out

            relu_out, cache[relu_cache] = relu_forward(h_out)              # 激活函数处理

            # dropout输出
            if self.use_dropout:
                dropout = 'keep%d_cache'%(num+1)
                drop_out, cache[dropout]= dropout_forward(relu_out, self.dropout_param)
                relu_out = drop_out

            layer_input = relu_out                                         # 更新下次传入的数据
        # 计算第L层的输出，无激活函数
        h_out, cache['h%d_cache'% (L)] = affine_forward(layer_input, self.params['W%d'% (L)], self.params['b%d'% (L)])
        scores = h_out
        pass

        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        # If test mode return early
        if mode == 'test':
            return scores

        loss, grads = 0.0, {}
        ############################################################################
        # TODO: Implement the backward pass for the fully-connected net. Store the #
        # loss in the loss variable and gradients in the grads dictionary. Compute #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        #                                                                          #
        # When using batch/layer normalization, you don't need to regularize the scale   #
        # and shift parameters.                                                    #
        #                                                                          #
        # NOTE: To ensure that your implementation matches ours and you pass the   #
        # automated tests, make sure that your L2 regularization includes a factor #
        # of 0.5 to simplify the expression for the gradient.                      #
        ############################################################################
        # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        """
        三个事情：
        1. Softmax 计算 loss.
        2. 保存计算 gradient 在 grads[k]
        3. L2正则化 (Loss 有两部分，要小心嗷)
        """
        loss, softmax_grads = softmax_loss(scores, y)               # 获取softmax的输出,数据损失和梯度
        # 先将第L层反向传播，因为该层无激活函数
        upstream_grads, grads['W%d'%L], grads['b%d'%L] = affine_backward(softmax_grads, cache['h%d_cache'% (L)])
        grads['W%d'%L] += self.reg * self.params['W%d'%L]                # 累加正则化部分
        regular_loss = np.sum(self.params['W%d'%L]*self.params['W%d'%L]) # 正则化损失

        for num in list(range(L-1))[::-1]:                          # 反向传播前L-1层，倒序访问网络
            W = 'W%d'% (num+1)
            b = 'b%d'% (num+1)
            regular_loss += np.sum(self.params[W]*self.params[W])   # 累积正则化损失
            # 反向传播Dropout层
            if self.use_dropout:
                upstream_grads = dropout_backward(upstream_grads, cache['keep%d_cache'%(num+1)])
            # 反向传播ReLU层
            upstream_grads = relu_backward(upstream_grads, cache['relu%d_cache'% (num+1)])

            # 反向传播BN层
            if self.normalization=='batchnorm':
                gamma = 'gamma%d'%(num+1)
                beta = 'beta%d'%(num+1)
                upstream_grads, grads[gamma], grads[beta]= batchnorm_backward_alt(upstream_grads, cache['bn%d_cache'%(num+1)])
            # 反向传播LN层
            if self.normalization=='layernorm':
                gamma = 'gamma%d'%(num+1)
                beta = 'beta%d'%(num+1)
                upstream_grads, grads[gamma], grads[beta]= layernorm_backward(upstream_grads, cache['ln%d_cache'%(num+1)])

            # 反向传播全连接层
            upstream_grads, grads[W], grads[b] = affine_backward(upstream_grads, cache['h%d_cache'% (num+1)])
            grads[W] += self.reg * self.params[W]  # 累加正则化梯度部分

        loss +=  0.5 * self.reg * regular_loss     # 总的损失函数


        # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads