#RISHAB KSHATRI
#PES2UG19CS327
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import math

"""
Use DecisionTreeClassifier to represent a stump.
------------------------------------------------
DecisionTreeClassifier Params:
    critereon -> entropy
    max_depth -> 1
    max_leaf_nodes -> 2
Use the same parameters
"""
# REFER THE INSTRUCTION PDF FOR THE FORMULA TO BE USED 

class AdaBoost:

    """
    AdaBoost Model Class
    Args:
        n_stumps: Number of stumps (int.)
    """

    def __init__(self, n_stumps=20):

        self.n_stumps = n_stumps
        self.stumps = []

    def fit(self, X, y):
        """
        Fitting the adaboost model
        Args:
            X: M x D Matrix(M data points with D attributes each)(numpy float)
            y: M Vector(Class target for all the data points as int.)
        Returns:
            the object itself
        """
        self.alphas = []

        sample_weights = np.ones_like(y) / len(y)
        for _ in range(self.n_stumps):

            st = DecisionTreeClassifier(
                criterion='entropy', max_depth=1, max_leaf_nodes=2)
            st.fit(X, y, sample_weights)
            y_pred = st.predict(X)

            self.stumps.append(st)

            error = self.stump_error(y, y_pred, sample_weights=sample_weights)
            alpha = self.compute_alpha(error)
            self.alphas.append(alpha)
            sample_weights = self.update_weights(
                y, y_pred, sample_weights, alpha)

        return self

    def stump_error(self, y, y_pred, sample_weights):
        """
        Calculating the stump error
        Args:
            y: M Vector(Class target for all the data points as int.)
            y_pred: M Vector(Class target predicted for all the data points as int.)
            sample_weights: M Vector(Weight of each sample float.)
        Returns:
            The error in the stump(float.)
        """


        
        if y.shape == y_pred.shape:
            k = (y==y_pred)  
            loss = np.multiply(np.logical_xor(k,np.ones_like(k)),1)
            error = np.dot(sample_weights,loss)
            return error
        

    def compute_alpha(self, error):
        """
        Computing alpha
        The weight the stump has in the final prediction
        Use eps = 1e-9 for numerical stabilty.
        Args:
            error:The stump error(float.)
        Returns:
            The alpha value(float.)
        """
        eps = 1e-9
        if error>0.0:
            eps = error
        alpha = 0.5 * math.log((1-eps)/eps)
        return alpha

    def update_weights(self, y, y_pred, sample_weights, alpha):
        """
        Updating Weights of the samples based on error of current stump
        The weight returned is normalized
        Args:
            y: M Vector(Class target for all the data points as int.)
            y_pred: M Vector(Class target predicted for all the data points as int.)
            sample_weights: M Vector(Weight of each sample float.)
            alpha: The stump weight(float.)
        Returns:
            new_sample_weights:  M Vector(new Weight of each sample float.)
        """

        if y.shape == y_pred.shape:
            k = (y==y_pred)
            c = np.multiply(k,1)
            c[c==1]=-1
            c[c==0]=+1
            updated_weights = np.multiply(sample_weights,np.exp(np.multiply(alpha,c)))
            final_wts = updated_weights / sum(updated_weights)
            return final_wts
   

    def predict(self, X):
        """
        Predicting using AdaBoost model with all the decision stumps.
        Decison stump predictions are weighted.
        Args:
            X: N x D Matrix(N data points with D attributes each)(numpy float)
        Returns:
            pred: N Vector(Class target predicted for all the inputs as int.)
        """

        alphas = self.alphas
        st = self.stumps
        arr = []
        pred =[]
        for i in st:
            y_pre = i.predict(X)
            arr.append(y_pre)
        arr = np.array(arr)

        for j in range(len(arr[0])):
            li = arr[:,j]
            pred.append(self.sigmoid(np.multiply(li,alphas)))
        return np.array(pred)

    
    def sigmoid(self,z):
        s = 1/(1+np.exp(-z))
        for i in s:
            if i<=0.5:
                return 0
            else:
                return 1

        

    def evaluate(self, X, y):
        """
        Evaluate Model on test data using
            classification: accuracy metric
        Args:
            x: Test data (N x D) matrix
            y: True target of test data
        Returns:
            accuracy : (float.)
        """
        pred = self.predict(X)
        # find correct predictions
        correct = (pred == y)

        accuracy = np.mean(correct) * 100  # accuracy calculation
        return accuracy