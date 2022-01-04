# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from km_insurance.pipelines import data_engineering as d_eng
from km_insurance.pipelines import data_ingestion as d_ing
from km_insurance.pipelines import data_segregation as d_seg
from km_insurance.pipelines import final_model as f_mod
from km_insurance.pipelines import model_evaluation as m_eva
from km_insurance.pipelines import prediction as pred


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    data_ingestion_pipeline = d_ing.create_pipeline()
    data_engineering_pipeline = d_eng.create_pipeline()
    data_segregation_pipeline = d_seg.create_pipeline()
    model_evaluation_pipeline = m_eva.create_pipeline()
    final_model_pipeline = f_mod.create_pipeline()
    prediction_pipeline = pred.create_pipeline()

    return {
        "d_ing": data_ingestion_pipeline,
        "d_eng": data_engineering_pipeline,
        "d_seg": data_segregation_pipeline,
        "m_eva": model_evaluation_pipeline,
        "f_mod": final_model_pipeline,
        "pred": prediction_pipeline,
        "__default__": data_ingestion_pipeline
        + data_engineering_pipeline
        + data_segregation_pipeline,
    }
