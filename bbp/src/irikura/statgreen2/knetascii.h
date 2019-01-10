// knetascii.h: knetascii クラスのインターフェイス
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_KNETASCII_H__06E791F4_023D_4921_839C_6B19975249BC__INCLUDED_)
#define AFX_KNETASCII_H__06E791F4_023D_4921_839C_6B19975249BC__INCLUDED_

#pragma warning ( disable : 4786 )

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include <string.h>
#include <vector>
#include <list>
#include <iostream>

using namespace std;

typedef	list<string>	string_list;

#define	HEADER_LINE_NUMBER	17
#define	LINE_LENGTH			72

typedef	enum kind_of_data {KNET_ACC, KNET_VEL, KNET_DIS, KNET_OTHER} KIND_OF_DATA;

class knetascii
{
public:
	KIND_OF_DATA	kind_of_data_;

private:
    string	origin_time_;
    double	epic_latitude_;
    double	epic_longitude_;
    double	epic_depth_;
    double	magnitude_;
    string	site_code_;
    double	site_latitude_;
    double	site_longitude_;
    double	site_height_;
    string	record_time_;
    int		sampling_frequency_;
    double	duration_;
    string	direction_;
    double	denominator_;
    double	numerator_;
    double	max_value_;
    string	last_correction_;
    string	memo_;

	vector<int>	data_;

public:
    knetascii();
    virtual ~knetascii();

	/// getter
    virtual	const string	get_origin_time(){return origin_time_;}
    virtual	double	get_epic_latitude(){return epic_latitude_;}
    virtual	double	get_epic_longitude(){return epic_longitude_;}
    virtual	double	get_epic_depth(){return epic_depth_;}
    virtual	double	get_magnitude(){return magnitude_;}
    virtual	const string	get_site_code(){return site_code_;}
    virtual	double	get_site_latitude(){return site_latitude_;}
    virtual	double	get_site_longitude(){return site_longitude_;}
    virtual	double	get_site_height(){return site_height_;}
    virtual	const string	get_record_time(){return record_time_;}
    virtual	int		get_sampling_frequency(){return sampling_frequency_;}
    virtual	double	get_duration(){return duration_;}
    virtual	const string	get_direction(){return direction_;}
    virtual	double	get_denominator(){return denominator_;}
    virtual	double	get_numerator(){return numerator_;}
    virtual	double	get_max_value(){return max_value_;}
    virtual	const string	get_last_correction(){return last_correction_;}
    virtual	const string	get_memo(){return memo_;}
	virtual void	get_data(vector<int>& data);
	virtual void	get_data(vector<double>& data);
	virtual const vector<int>& get_rawdata() const { return data_; }
	virtual double  get_amplitude( int i ) const { return denominator_/numerator_*data_[i]; }


	/// setter
    virtual	void	set_origin_time(string origin){origin_time_ = origin;}
    virtual	void	set_epic_latitude(double lat){epic_latitude_ = lat;}
    virtual	void	set_epic_longitude(double lng){epic_longitude_ = lng;}
    virtual	void	set_epic_depth(double dep){epic_depth_ = dep;}
    virtual	void	set_magnitude(double mag){magnitude_ = mag;}
    virtual	void	set_site_code(string code){site_code_ = code;}
    virtual	void	set_site_latitude(double lat){site_latitude_ = lat;}
    virtual	void	set_site_longitude(double lng){site_longitude_ = lng;}
    virtual	void	set_site_height(double hgt){site_height_ = hgt;}
    virtual	void	set_record_time(string record){record_time_ = record;}
    virtual	void	set_sampling_frequency(int sampling){sampling_frequency_ = sampling;}
    virtual	void	set_duration(double duration){duration_ = duration;}
    virtual	void	set_direction(string dir){direction_ = dir;}
    virtual	void	set_denominator(double deno){denominator_ = deno;}
    virtual	void	set_numerator(double num){numerator_ = num;}
    virtual	void	set_max_value(double val){max_value_ = val;}
    virtual	void	set_last_correction(string correction){last_correction_ = correction;}
    virtual	void	set_memo(string memo){memo_ = memo;}
	virtual void	set_data(vector<int> data){data_=data;}
	virtual void	set_data(vector<double> data);
	virtual void	push_back(int data){data_.push_back(data);}
	virtual void	clear_data(){data_.clear();}

    virtual	string_list	make_header();

    friend	ostream& operator<<(ostream& strm, knetascii& knet);
    friend	istream& operator>>(istream& strm, knetascii& knet);
};

#endif // !defined(AFX_KNETASCII_H__06E791F4_023D_4921_839C_6B19975249BC__INCLUDED_)
