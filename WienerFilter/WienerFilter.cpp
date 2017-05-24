#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <assert.h>
#include <time.h>

using namespace cv;
using namespace std;

double WienerFilter(const Mat& src, Mat& dst, const Size& block){

	assert(("src and dst must be one channel grayscale images", src.channels() == 1, dst.channels() == 1));

	int h = src.rows;
	int w = src.cols;
	double noiseVariance;

	dst = Mat1b(h, w);

	Mat1d means, sqrMeans, variances;
	Mat1d avgVarianceMat;

	boxFilter(src, means, CV_64F, block, Point(-1, -1), true, BORDER_REPLICATE);
	sqrBoxFilter(src, sqrMeans, CV_64F, block, Point(-1, -1), true, BORDER_REPLICATE);

	Mat1d means2 = means.mul(means);
	variances = sqrMeans - (means.mul(means));

	reduce(variances, avgVarianceMat, 1, CV_REDUCE_SUM, -1);
	reduce(avgVarianceMat, avgVarianceMat, 0, CV_REDUCE_SUM, -1);
	noiseVariance = avgVarianceMat(0, 0) / (h*w);

	for (int r = 0; r < h; ++r){
		// get row pointers
		uchar const * const srcRow = src.ptr<uchar>(r);
		uchar * const dstRow = dst.ptr<uchar>(r);
		double * const varRow = variances.ptr<double>(r);
		double * const meanRow = means.ptr<double>(r);
		for (int c = 0; c < w; ++c) {
			dstRow[c] = saturate_cast<uchar>(
				meanRow[c] + max(0., varRow[c] - noiseVariance) / max(varRow[c], noiseVariance) * (srcRow[c] - meanRow[c])
			);
		}
	}

	return noiseVariance;
}


int main(int argc, char** argv)
{

	if(argc != 2)
	{
		cout << "Usage: WienerFilter <Image_Path>" << endl;
		return -1;
	}

	string testImage = argv[1];
	Mat1b src = imread(testImage, CV_LOAD_IMAGE_GRAYSCALE);
	Mat1b dst5x5;

	if (src.empty()){
		cout << "The specified image '" << testImage << "' does not exists" << endl;
		exit(-1);
	}

	struct timespec start, finish;
  double elapsed;
  clock_gettime(CLOCK_MONOTONIC, &start);

  WienerFilter(src, dst5x5, Size(5,5));

  clock_gettime(CLOCK_MONOTONIC, &finish);
  elapsed = (finish.tv_sec - start.tv_sec);
  elapsed += (finish.tv_nsec - start.tv_nsec) / 1000000000.0;

  imwrite("WienerFiltered.png", dst5x5);

  cout << "Finished in " << elapsed << " seconds" << endl;

	return 0;
}
