package com.schedutn.scheduler.api.jsonapi

/**
 *  JSON:API relationships.
 *
 */
interface JsonApiRelationShip

/**
 * JSON:API base format
 *
 * @param T type of attributes
 */
abstract class AbstractJsonApiData<T> {

  /**
   * Unique resource identifier.
   */
  abstract val id: String

  /**
   * Resource attributes.
   */
  abstract val attributes: T?

  /**
   * Resource relationships.
   */
  abstract val relationships: JsonApiRelationShip?

  /**
   * Resource type.
   */
  abstract val type: String
}

/**
 * JSON:API resource format.
 *
 * @param T type of Data attributes
 */
abstract class AbstractJsonApiResource<T> {

  /**
   * Resource data.
   */
  abstract val data: AbstractJsonApiData<T>
}

/**
 * JSON:API resources format.
 *
 * @param T type of Data attributes
 */
abstract class AbstractJsonApiResources<T> {

  /**
   * Resources data.
   */
  abstract val data: Collection<AbstractJsonApiData<T>>
}