//Don't Edit it

#include "test.h"
#include "network/net_util/json_serializer_helper.hpp"


namespace net {
namespace test {

Thumbnail::Thumbnail():		height(0){
}

void Thumbnail::Serialize(
		JsonSerializerHelper& json_serializer_helper) const {
	json_serializer_helper.SerializeNVP(url);
	json_serializer_helper.SerializeNVP(width);
	json_serializer_helper.SerializeNVP(height);
}

void Thumbnail::DeSerialize(
		const JsonSerializerHelper& json_serializer_helper) {
	json_serializer_helper.DeSerializeNVP(url);
	json_serializer_helper.DeSerializeNVP(width);
	json_serializer_helper.DeSerializeNVP(height);
}


Image::Image():		width(0),
		height(0){
}

void Image::Serialize(
		JsonSerializerHelper& json_serializer_helper) const {
	json_serializer_helper.SerializeNVP(ids);
	json_serializer_helper.SerializeNVP(width);
	json_serializer_helper.SerializeNVP(title);
	json_serializer_helper.SerializeNVP(thumbnail);
	json_serializer_helper.SerializeNVP(height);
}

void Image::DeSerialize(
		const JsonSerializerHelper& json_serializer_helper) {
	json_serializer_helper.DeSerializeNVP(ids);
	json_serializer_helper.DeSerializeNVP(width);
	json_serializer_helper.DeSerializeNVP(title);
	json_serializer_helper.DeSerializeNVP(thumbnail);
	json_serializer_helper.DeSerializeNVP(height);
}


Test::Test(){
}

void Test::Serialize(
		JsonSerializerHelper& json_serializer_helper) const {
	json_serializer_helper.SerializeNVP(image);
}

void Test::DeSerialize(
		const JsonSerializerHelper& json_serializer_helper) {
	json_serializer_helper.DeSerializeNVP(image);
}


} // namespace test
} // namespace net
