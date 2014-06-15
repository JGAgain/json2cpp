// Don't Edit it
#ifndef TEST_H_
#define TEST_H_

#include <string>
#include <vector>
#include <lib_json/json_lib.h>


class JsonSerializerHelper;

namespace net {
namespace test {


class Thumbnail {
 public:
	Thumbnail();
	~Thumbnail(){}

	const std::string& get_url() { return url;}
	const std::string& get_url() const { return url;}
	void set_url(const std::string& url_a) {
		 url = url_a; 
	}

	const std::string& get_width() { return width;}
	const std::string& get_width() const { return width;}
	void set_width(const std::string& width_a) {
		 width = width_a; 
	}

	const int& get_height() { return height;}
	const int& get_height() const { return height;}
	void set_height(const int& height_a) {
		 height = height_a; 
	}


	void Serialize(JsonSerializerHelper& json_serializer_helper) const;
	void DeSerialize(const JsonSerializerHelper& json_serializer_helper);

 private:
	 std::string url;
	 std::string width;
	 int height;

}; // class Thumbnail

class Image {
 public:
	Image();
	~Image(){}

	const std::vector<int>& get_ids() { return ids;}
	const std::vector<int>& get_ids() const { return ids;}
	void set_ids(const std::vector<int>& ids_a) {
		 ids = ids_a; 
	}

	const int& get_width() { return width;}
	const int& get_width() const { return width;}
	void set_width(const int& width_a) {
		 width = width_a; 
	}

	const std::string& get_title() { return title;}
	const std::string& get_title() const { return title;}
	void set_title(const std::string& title_a) {
		 title = title_a; 
	}

	Thumbnail& get_thumbnail() { return thumbnail;}
	const Thumbnail& get_thumbnail() const { return thumbnail;}
	void set_thumbnail(const Thumbnail& thumbnail_a) {
		 thumbnail = thumbnail_a; 
	}

	const int& get_height() { return height;}
	const int& get_height() const { return height;}
	void set_height(const int& height_a) {
		 height = height_a; 
	}


	void Serialize(JsonSerializerHelper& json_serializer_helper) const;
	void DeSerialize(const JsonSerializerHelper& json_serializer_helper);

 private:
	 std::vector<int> ids;
	 int width;
	 std::string title;
	 Thumbnail thumbnail;
	 int height;

}; // class Image

class Test {
 public:
	Test();
	~Test(){}

	Image& get_image() { return image;}
	const Image& get_image() const { return image;}
	void set_image(const Image& image_a) {
		 image = image_a; 
	}


	void Serialize(JsonSerializerHelper& json_serializer_helper) const;
	void DeSerialize(const JsonSerializerHelper& json_serializer_helper);

 private:
	 Image image;

}; // class Test

} // namespace test
} // namespace net
#endif // TEST_H_
